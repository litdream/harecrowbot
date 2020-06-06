import pytest
import bot_version

def test_version():
    ctx = None    # we need mock
    v = bot_version.Version(ctx)
    v.major = 1
    v.minor = 2
    assert( v.version() == 'harecrowbot v1.2' )

def test_version_with_release():
    ctx = None    # we need mock
    v = bot_version.Version(ctx)
    v.major = 1
    v.minor = 2
    v.release = 1
    assert( v.version() == 'harecrowbot v1.2r1' )
    
