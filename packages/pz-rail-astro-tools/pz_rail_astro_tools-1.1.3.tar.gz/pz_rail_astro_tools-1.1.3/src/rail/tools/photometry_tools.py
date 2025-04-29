"""
Module that implements operations on photometric data such as magnitudes and fluxes.
"""
from abc import ABC, abstractmethod

import os
import numpy as np
import pandas as pd
import tables_io
from astropy.coordinates import SkyCoord

from ceci.config import StageParameter as Param
from rail.core.data import PqHandle
from rail.core.stage import RailStage
from rail.core.data import PqHandle, Hdf5Handle
from rail.core.common_params import SHARED_PARAMS

import hyperbolic  # https://github.com/jlvdb/hyperbolic

dustmaps_config = tables_io.lazy_modules.lazyImport('dustmaps.config')
dustmaps_sfd = tables_io.lazy_modules.lazyImport('dustmaps.sfd')


# default column names in DC2
LSST_BANDS = 'ugrizy'
DEFAULT_MAG_COLS = [f"mag_{band}_lsst" for band in LSST_BANDS]
DEFAULT_MAGERR_COLS = [f"mag_err_{band}_lsst" for band in LSST_BANDS]


def _compute_flux(magnitude, zeropoint):
    """
    Compute the flux corresponding to a given magnitude and photometric zeropoint.

    Parameters
    ----------
    magnitude : array-like
        Magnitude or array of magnitudes.
    zeropoint : array-like
        Photometric zeropoint used for conversion.

    Returns
    -------
    flux : array-like
        Flux value(s).
    """
    flux = np.exp((zeropoint - magnitude) / hyperbolic.pogson)
    return flux


def _compute_flux_error(flux, magnitude_error):
    """
    Compute the flux error corresponding to a given flux and magnitude error.

    Parameters
    ----------
    flux : array-like
        Flux or array of fluxes.
    magnitude_error : array-like
        Magnitude error or array of magnitude errors.

    Returns
    -------
    flux_error : array-like
        Flux error value(s).
    """
    flux_error = magnitude_error / hyperbolic.pogson * flux
    return flux_error


class PhotometryManipulator(RailStage, ABC):
    """
    Base class to perform opertations on magnitudes. A table with input magnitudes and errors is
    processed and transformed into an output table with new magnitudes and errors.

    Subclasses must implement the run() and compute() method.
    """

    name = 'PhotometryManipulator'
    config_options = RailStage.config_options.copy()
    config_options.update(
        value_columns=Param(
            list, default=DEFAULT_MAG_COLS,
            msg="list of columns that prove photometric measurements (fluxes or magnitudes)"),
        error_columns=Param(
            list, default=DEFAULT_MAGERR_COLS,
            msg="list of columns with errors corresponding to value_columns "
                "(assuming same ordering)"),
        zeropoints=Param(
            list, default=[], required=False,
            msg="optional list of magnitude zeropoints for value_columns "
                "(assuming same ordering, defaults to 0.0)"),
        is_flux=Param(
            bool, default=False,
            msg="whether the provided quantities are fluxes or magnitudes"))
    inputs = [('input', PqHandle)]
    outputs = [('output', PqHandle)]

    def __init__(self, args, **kwargs):
        super().__init__(args, **kwargs)
        self._check_config()
        # convenience remapping of parameters
        self.value_columns = self.config.value_columns
        self.error_columns = self.config.error_columns
        self.zeropoints = self.config.zeropoints
        self.n_col = len(self.value_columns)

    def _check_config(self):
        # compare column definitions
        n_mag = len(self.config.value_columns)
        n_err = len(self.config.error_columns)
        n_zpt = len(self.config.zeropoints)
        if n_mag != n_err:
            raise IndexError(
                f"number of magnitude and error columns do not match ({n_mag} != {n_err})")
        # check and zeropoints or parse default value
        if n_zpt == 0:
            self.config.zeropoints = [0.0] * n_mag
        elif n_zpt != n_mag:
            raise IndexError(
                f"number of zeropoints and magnitude columns do not match ({n_zpt} != {n_mag})")

    def get_as_fluxes(self):
        """
        Loads specified photometric data as fluxes, converting magnitudes on the fly.
        """
        input_data = self.get_data('input', allow_missing=True)
        if self.config.is_flux:
            data = input_data[self.value_columns + self.error_columns]
        else:
            data = pd.DataFrame()
            # convert magnitudes to fluxes
            for val_name, zeropoint in zip(self.value_columns, self.zeropoints):
                data[val_name] = _compute_flux(
                    input_data[val_name],
                    zeropoint=zeropoint)
            # compute flux errors from magnitude errors
            for val_name, err_name in zip(self.value_columns, self.error_columns):
                data[err_name] = _compute_flux_error(
                    data[val_name],
                    input_data[err_name])
        return data

    @abstractmethod
    def run(self):  # pragma: no cover
        """
        Implements the operation performed on the photometric data.
        """
        data = self.get_as_fluxes()
        # do work
        self.add_data('output', data)

    @abstractmethod
    def compute(self, data):  # pragma: no cover
        """
        Main method to call.

        Parameters
        ----------
        data : `PqHandle`
           Input tabular data with column names as defined in the configuration.

        Returns
        -------
        output: `PqHandle`
            Output tabular data.
        """
        self.set_data('input', data)
        self.run()
        self.finalize()
        return self.get_handle('output')


class HyperbolicSmoothing(PhotometryManipulator):
    """
    Initial stage to compute hyperbolic magnitudes (Lupton et al. 1999). Estimates the smoothing
    parameter b that is used by the second stage (`HyperbolicMagnitudes`) to convert classical to
    hyperbolic magnitudes.
    """

    name = 'HyperbolicSmoothing'
    config_options = PhotometryManipulator.config_options.copy()
    inputs = [('input', PqHandle)]
    outputs = [('parameters', PqHandle)]

    def run(self):
        """
        Computes the smoothing parameter b (see Lupton et al. 1999) per photometric band.
        """
        # get input data
        data = self.get_as_fluxes()
        fields = np.zeros(len(data), dtype=int)  # placeholder

        # compute the optimal smoothing factor b for each photometric band
        stats = []
        for fx_col, fxerr_col, zeropoint in zip(
                self.value_columns, self.error_columns, self.zeropoints):

            # compute the median flux error and zeropoint
            stats_filt = hyperbolic.compute_flux_stats(
                data[fx_col], data[fxerr_col], fields, zeropoint=zeropoint)
            # compute the smoothing parameter b (in normalised flux)
            stats_filt[hyperbolic.Keys.b] = hyperbolic.estimate_b(
                stats_filt[hyperbolic.Keys.zp],
                stats_filt[hyperbolic.Keys.flux_err])
            # compute the smoothing parameter b (in absolute flux)
            stats_filt[hyperbolic.Keys.b_abs] = (
                stats_filt[hyperbolic.Keys.ref_flux] *
                stats_filt[hyperbolic.Keys.b])

            # collect results
            stats_filt[hyperbolic.Keys.filter] = fx_col
            stats_filt = stats_filt.reset_index().set_index([
                hyperbolic.Keys.filter,
                hyperbolic.Keys.field])
            stats.append(stats_filt)

        # store resulting smoothing parameters for next stage
        self.add_data('parameters', pd.concat(stats))

    def compute(self, data):
        """
        Main method to call. Computes the set of smoothing parameters (b) for an input catalogue
        with classical photometry and their respective errors. These parameters are required by the
        follow-up stage `HyperbolicMagnitudes` and are parsed as tabular data.

        Parameters
        ----------
        data : `PqHandle`
            Input table with magnitude and magnitude error columns as defined in the configuration.

        Returns
        -------
        parameters : `PqHandle`
            Table with smoothing parameters per photometric band and additional meta data.
        """
        self.set_data('input', data)
        self.run()
        self.finalize()
        return self.get_handle('parameters')


class HyperbolicMagnitudes(PhotometryManipulator):
    """
    Convert a set of classical magnitudes to hyperbolic magnitudes  (Lupton et al. 1999). Requires
    input from the initial stage (`HyperbolicSmoothing`) to supply optimal values for the smoothing
    parameters (b).
    """

    name = 'HyperbolicMagnitudes'
    config_options = PhotometryManipulator.config_options.copy()
    inputs = [('input', PqHandle),
              ('parameters', PqHandle)]
    outputs = [('output', PqHandle)]

    def _check_filters(self, stats_table):
        """
        Check whether the column definition matches the loaded smoothing parameters.

        Parameters:
        -----------
        stats_table : `pd.DataFrame`
            Data table that contains smoothing parameters per photometric band (from
            `HyperbolicSmoothing`).

        Raises
        ------
        KeyError : Filter defined in magnitude_columns is not found in smoothing parameter table.
        """
        # filters in the parameter table
        param_filters = set(stats_table.reset_index()[hyperbolic.Keys.filter])
        # filters parsed through configuration
        config_filters = set(self.value_columns)
        # check if the filters match
        filter_diff = config_filters - param_filters
        if len(filter_diff) != 0:
            strdiff = ", ".join(sorted(filter_diff))
            raise KeyError(f"parameter table contains no smoothing parameters for: {strdiff}")

    def run(self):
        """
        Compute hyperbolic magnitudes and their error based on the parameters determined by
        `HyperbolicSmoothing`.
        """
        # get input data
        data = self.get_as_fluxes()
        stats = self.get_data('parameters', allow_missing=True)
        self._check_filters(stats)
        fields = np.zeros(len(data), dtype=int)  # placeholder for variable field/pointing depth

        # intialise the output data
        output = pd.DataFrame(index=data.index)  # allows joining on input

        # compute smoothing parameter b
        b = stats[hyperbolic.Keys.b].groupby(  # median flux error in each filter
            hyperbolic.Keys.filter).agg(np.nanmedian)
        b = b.to_dict()

        # hyperbolic magnitudes
        for val_col, err_col in zip(self.value_columns, self.error_columns):
            # get the smoothing parameters
            stats_filt = hyperbolic.fill_missing_stats(stats.loc[val_col])

            # map reference flux from fields/pointings to sources
            ref_flux_per_source = hyperbolic.fields_to_source(
                stats_filt[hyperbolic.Keys.ref_flux], fields, index=data.index)
            norm_flux = data[val_col] / ref_flux_per_source
            norm_flux_err = data[err_col] / ref_flux_per_source

            # compute the hyperbolic magnitudes
            hyp_mag = hyperbolic.compute_magnitude(
                norm_flux, b[val_col])
            hyp_mag_err = hyperbolic.compute_magnitude_error(
                norm_flux, b[val_col], norm_flux_err)

            # add data to catalogue
            key_mag = val_col.replace("mag_", "mag_hyp_")
            key_mag_err = err_col.replace("mag_", "mag_hyp_")
            output[key_mag] = hyp_mag
            output[key_mag_err] = hyp_mag_err

        # store results
        self.add_data('output', output)

    def compute(self, data, parameters):
        """
        Main method to call. Outputs hyperbolic magnitudes compuated from a set of smoothing
        parameters and input catalogue with classical magitudes and their respective errors.

        Parameters
        ----------
        data : `PqHandle`
            Input table with photometry (magnitudes or flux columns and their respective
            uncertainties) as defined by the configuration.
        parameters : `PqHandle`
            Table witdh smoothing parameters per photometric band, determined by
            `HyperbolicSmoothing`.

        Returns
        -------
        output: `PqHandle`
            Output table containting hyperbolic magnitudes and their uncertainties. If the columns
            in the input table contain a prefix `mag_`, this output tabel will replace the prefix
            with `hyp_mag_`, otherwise the column names will be identical to the input table.
        """
        self.set_data('input', data)
        self.set_data('parameters', parameters)
        self.run()
        self.finalize()
        return self.get_handle('output')


class LSSTFluxToMagConverter(RailStage):
    """Utility stage that converts from fluxes to magnitudes

    Note, this is hardwired to take parquet files as input
    and provide hdf5 files as output
    """
    name = 'LSSTFluxToMagConverter'

    config_options = RailStage.config_options.copy()
    config_options.update(
        bands=Param(str, default='ugrizy', msg="Names of the bands"),
        flux_name=Param(str, default="{band}_gaap1p0Flux", msg="Template for band names"),
        flux_err_name=Param(str, default="{band}_gaap1p0FluxErr", msg="Template for band error column names"),
        mag_name=Param(str, default="mag_{band}_lsst", msg="Template for magnitude column names"),
        mag_err_name=Param(str, default="mag_err_{band}_lsst", msg="Template for magnitude error column names"),
        copy_cols=Param(dict, default={}, msg="Map of other columns to copy"),
        mag_offset=Param(float, default=31.4, msg="Magntidue offset value"),
    )

    mag_conv = np.log(10)*0.4

    inputs = [('input', PqHandle)]
    outputs = [('output', PqHandle)]

    def _flux_to_mag(self, flux_vals):
        vals = -2.5*np.log10(flux_vals) + self.config.mag_offset
        return np.where(np.isfinite(vals), vals, np.nan)

    def _flux_err_to_mag_err(self, flux_vals, flux_err_vals):
        return flux_err_vals / (flux_vals*self.mag_conv)

    def run(self):
        data = self.get_data('input', allow_missing=True)
        out_data = {}
        const = np.log(10.)*0.4

        for band_ in self.config.bands:
            flux_col_name = self.config.flux_name.format(band=band_)
            flux_err_col_name = self.config.flux_err_name.format(band=band_)
            out_data[self.config.mag_name.format(band=band_)] = self._flux_to_mag(data[flux_col_name].values)
            out_data[self.config.mag_err_name.format(band=band_)] = self._flux_err_to_mag_err(data[flux_col_name].values, data[flux_err_col_name].values)
        for key, val in self.config.copy_cols.items():  # pragma: no cover
            out_data[key] = data[val].values
        self.add_data('output', out_data)

    def __call__(self, data):
        """Return a converted table

        Parameters
        ----------
        data : table-like
            The data to be converted

        Returns
        -------
        out_data : table-like
            The converted version of the table
        """
        self.set_data('input', data)
        self.run()
        return self.get_handle('output')


class DustMapBase(RailStage):
    """Utility stage that does dereddening
    
    Note: set copy_all_cols=True to copy all 
    columns in data, copy_cols will be ignored
    """
    name = 'DustMapBase'

    config_options = RailStage.config_options.copy()
    config_options.update(
        ra_name=Param(str, default='ra', msg="Name of the RA column"),
        dec_name=Param(str, default='dec', msg="Name of the DEC column"),
        mag_name=Param(str, default="mag_{band}_lsst", msg="Template for the magnitude columns"),
        band_a_env=SHARED_PARAMS,
        dustmap_name=Param(str, default='sfd', msg="Name of the dustmap in question"),
        dustmap_dir=Param(str, required=True, msg="Directory with dustmaps"),
        copy_cols=Param(list, default=[], msg="Additional columns to copy"),
        copy_all_cols=Param(bool, default=False, msg="Copy all the columns"),
    )
        
    inputs = [('input', PqHandle)]
    outputs = [('output', PqHandle)]

    def fetch_map(self):
        dust_map_dict = dict(sfd=dustmaps_sfd)
        try:
            dust_map_submod = dust_map_dict[self.config.dustmap_name]
        except KeyError as msg:  # pragma: no cover
            raise KeyError(f"Unknown dustmap {self.config.dustmap_name}, options are {list(dust_map_dict.keys())}") from msg

        dustmap_dir = os.path.expandvars(self.config.dustmap_dir)
        dustmap_path = os.path.join(dustmap_dir, self.config.dustmap_name)
        if os.path.exists(dustmap_path):  # pragma: no cover
            # already downloaded, return
            return
        
        dust_map_config = dustmaps_config.config
        # dust_map_config['data_dir'] = self.config.dustmap_dir
        dust_map_config['data_dir'] = dustmap_dir
        fetch_func = dust_map_submod.fetch
        fetch_func()
        

    def run(self):
        data = self.get_data('input', allow_missing=True)
        out_data = {}
        coords = SkyCoord(
            np.array(data[self.config.ra_name]),
            np.array(data[self.config.dec_name]),
            unit = 'deg',frame='fk5')
        dust_map_dict = dict(sfd=dustmaps_sfd.SFDQuery)
        try:
            dust_map_class = dust_map_dict[self.config.dustmap_name]
            dust_map_config = dustmaps_config.config
            dust_map_config['data_dir'] = self.config.dustmap_dir
            dust_map = dust_map_class()
        except KeyError as msg:  # pragma: no cover
            raise KeyError(f"Unknown dustmap {self.config.dustmap_name}, options are {list(dust_map_dict.keys())}") from msg
        ebvvec = dust_map(coords)
        band_mag_name_list=[]
        for band_mag_name, a_env_value in self.config.band_a_env.items():
            mag_vals = data[band_mag_name]
            out_data[band_mag_name] = self._calc_values(mag_vals, ebvvec, a_env_value)
            band_mag_name_list.append(band_mag_name)
       
        # check if copy_all_cols set to true:
        if self.config.copy_all_cols==False: # pragma: no cover
            for col_ in self.config.copy_cols:  # pragma: no cover
                out_data[col_] = data[col_]
        elif self.config.copy_all_cols==True: # pragma: no cover
            for col_ in data:
                # make sure we do not overwrite the photometry columns
                if col_ not in band_mag_name_list:
                    out_data[col_] = data[col_]

        out_data_pd = pd.DataFrame(out_data)
        self.add_data('output', out_data_pd)

    def __call__(self, data):
        """Return a converted table

        Parameters
        ----------
        data : table-like
            The data to be converted

        Returns
        -------
        out_data : table-like
            The converted version of the table
        """
        self.set_data('input', data)
        self.run()
        return self.get_handle('output')


class Dereddener(DustMapBase):
    """Utility stage that does dereddening
    
    """
    name = 'Dereddener'

    def _calc_values(self, mag_vals, ebvvec, band_a_env):
        return mag_vals - ebvvec*band_a_env
    

class Reddener(DustMapBase):
    """Utility stage that does reddening
    
    """
    name = 'Reddener'

    def _calc_values(self, mag_vals, ebvvec, band_a_env):
        return mag_vals + ebvvec*band_a_env
