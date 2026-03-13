
from pathlib import Path

import numpy as np
import pytest

from pypeit.scripts import loader

def test_load_spectra(redux_out):
    std_file = (
        Path(redux_out).absolute() / 'shane_kast_blue' / '600_4310_d55' / 'shane_kast_blue_A'
        / 'Science' / 'spec1d_b24-Feige66_KASTb_20150520T041246.960.fits'
    )
    assert std_file.is_file(), 'Spec1D file of standard star not produced'

    hdr, spec = loader.load_spectra(std_file)
    assert len(spec) == 3, 'Should have extracted 3 spectra'
    assert np.all(np.isin(['DISPNAME', 'fluxed', 'ext_mode'], list(spec[1].meta.keys()))), \
        'DISPNAME, fluxed, and ext_mode should all be keywords in the spectrum metadata dictionary'

    # Specifically request the uncalibrated boxcar extraction
    hdr, spec = loader.load_spectra(std_file, extract='BOX', fluxed=False)
    assert len(spec) == 3, 'Should have extracted 3 spectra'
    assert spec[1].meta['ext_mode'] == 'BOX', 'Should be the boxcar extraction'
    assert not spec[1].meta['fluxed'], 'Should be the uncalibrated spectrum'

