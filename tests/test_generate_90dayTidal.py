import unittest
from AdcircPyTests import AdcircPyEnvironment
from datetime import datetime, timedelta
from AdcircPy import AdcircPy
from AdcircPy import ElevationStationsOutput as ESO
from AdcircPy import ElevationGlobalOutput as EGO


class Generate90DayTidal(AdcircPyEnvironment, unittest.TestCase):
  def setUp(self):
    super(Generate90DayTidal, self).__init__()
    self.read_environment_variables()
    self.AdcircMesh = AdcircPy.read_mesh(fort14=self.os.getenv('FORT14_PATH'), fort13=self.os.getenv('FORT13_PATH'))
    self.ElevationStationsOutput = ESO.from_fort15(self.os.getenv('FORT15_HOTSTART_PATH'), harmonic_analysis=True)
    self.ElevationGlobalOutput = EGO(harmonic_analysis=True)

  def test_generate_90DayTidal(self):
    # Datetime is the same as the HSOFS offical 90 day tidal run.
    spinup_date = datetime(2013, 8, 1, 0, 0, 0)
    start_time  = spinup_date + timedelta(days=30)
    end_time    = spinup_date + timedelta(days=90)
    
    TidalRun = self.AdcircMesh.generate_tidal_run(start_time, end_time, spinup_date=spinup_date,
                                          ElevationStationsOutput=self.ElevationStationsOutput,
                                          ElevationGlobalOutput=self.ElevationGlobalOutput)
    TidalRun.dump("./", printf=True)
    self.os.remove('./fort.15.coldstart')
    self.os.remove('./fort.15.hotstart')

if __name__ == '__main__':
    unittest.main()