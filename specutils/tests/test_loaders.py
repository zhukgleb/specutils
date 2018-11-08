import numpy as np
from astropy.table import Table
import astropy.units as u
import pytest
from astropy.utils.data import get_pkg_data_filename

from .. import Spectrum1D
from .conftest import remote_data_path


@pytest.mark.parametrize('remote_data_path',
                         [
                             {'id': '1481190', 'filename': 'L5g_0355+11_Cruz09.fits'}
                         ],
                         indirect=True, scope='function')
def test_spectrum1d_GMOSfits(remote_data_path):
    optical_spec_2 = Spectrum1D.read(remote_data_path, format='wcs1d-fits')

    assert len(optical_spec_2.data) == 3020


@pytest.mark.parametrize('remote_data_path',
                         [
                             {'id': '1481190', 'filename': 'L5g_0355+11_Cruz09.fits'}
                         ],
                         indirect=True, scope='function')
def test_specific_spec_axis_unit(remote_data_path):
    optical_spec = Spectrum1D.read(remote_data_path,
                                   spectral_axis_unit="Angstrom",
                                   format='wcs1d-fits')

    assert optical_spec.spectral_axis.unit == "Angstrom"

def test_generic_ecsv_reader(tmpdir):
   # Create a small data set
   wave = np.arange(1,1.1,0.01)*u.AA
   flux = np.ones(len(wave))*1.e-14*u.Jy
   uncertainty = 0.01*flux
   table = Table([wave,flux,uncertainty],names=["wave","flux","uncertainty"])
   tmpfile = str(tmpdir.join('_tst.ecsv'))
   table.write(tmpfile,format='ascii.ecsv')

   # Read it in and check against the original
   spectrum = Spectrum1D.read(tmpfile,format='generic-ecsv')
   assert spectrum.spectral_axis.unit == table['wave'].unit
   assert spectrum.flux.unit == table['flux'].unit
   assert spectrum.uncertainty.unit == table['uncertainty'].unit
   assert spectrum.spectral_axis.unit == table['wave'].unit
   assert np.alltrue(spectrum.spectral_axis == table['wave'])
   assert np.alltrue(spectrum.flux == table['flux'])
   assert np.alltrue(spectrum.uncertainty.array == table['uncertainty'])

@pytest.mark.parametrize('remote_data_path',
                         [
                             {'id': '1481119', 'filename': 'COS_FUV.fits'},
                             {'id': '1481181', 'filename': 'COS_NUV.fits'}
                         ],
                         indirect=True, scope='function')
def test_hst_cos(remote_data_path):
    spec = Spectrum1D.read(remote_data_path, format='HST/COS')

    assert isinstance(spec, Spectrum1D)
    assert spec.flux.size > 0


@pytest.mark.parametrize('remote_data_path',
                         [
                             {'id': '1481192', 'filename':'STIS_FUV.fits'},
                             {'id': '1481185', 'filename': 'STIS_NUV.fits'},
                             {'id': '1481183', 'filename': 'STIS_CCD.fits'},
                         ],
                         indirect=True, scope='function')
def test_hst_stis(remote_data_path):
    spec = Spectrum1D.read(remote_data_path, format='HST/STIS')

    assert isinstance(spec, Spectrum1D)
    assert spec.flux.size > 0