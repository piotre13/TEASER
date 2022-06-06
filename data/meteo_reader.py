import pandas as pd

class MeteoReader(object):
    def __init__(self, path, batch, ts):
        self.path = path
        self.csv = None
        self.read()
        self.resample_interpolate(batch, ts)

    def read (self):
        self.csv = pd.read_csv(self.path)
    def C2K(self, column):
        self.csv[column] = self.csv[column].apply(lambda x: x + 273.1500)

    def conv_Wind(self, column):
        self.csv[column] = self.csv[column].apply(lambda x: x * 3.14159265359 / 180.0)

    def conv_Cvr(self, column):
        self.csv[column] = self.csv[column].apply(lambda x: x * 0.1)

    def add_forFMU(self):
        self.csv['TSetCool'] =299.1500
        self.csv['TSetHeat'] = 293.1500
        self.csv['fluPor[1].forward.T'] = 0.0
        self.csv['fluPor[2].forward.T'] = 0.0
        self.csv['fluPor[1].m_flow'] = 0.0
        self.csv['fluPor[2].m_flow'] = 0.0
        self.csv['heatCoolRoom_in']= 0.0
        self.csv['machinesConv_in']= 0.0
        self.csv['personsRad_in']= 0.0
        self.csv['personsConv_in']= 0.0
        self.csv['windowIndoorSurface_in'] = 0.0
        self.csv['extWallIndoorSurface_in']=0.0
        self.csv['intWallIndoorSurface_in']=0.0


    def save_csv(self):
        self.csv.to_csv('test_meteo_fmpyGUI.csv')

    def resample_interpolate(self, batch, ts):
        self.csv['DateTime'] = pd.to_datetime(self.csv['DateTime'])
        self.csv = self.csv.set_index('DateTime')
        self.csv = self.csv.head(batch)
        self.csv = self.csv.resample(ts).interpolate('akima')
        self.csv = self.csv.reset_index()

    def get_value(self, index, col_name):
        val = self.csv.loc[index, col_name]
        return val
    def get_row(self, index):
        row = self.csv.loc[index]
        return row


if __name__ == '__main__':
    path = '/home/pietrorm/Documents/CODE/TEASER/data/test_timeseries_meteo.csv'
    meteo = MeteoReader(path,24, '1H')
    #meteo.read()
    #print(meteo.csv.head())
    meteo.C2K('DryBulb')
    meteo.C2K('DewPoint')
    meteo.conv_Wind('WindDir')
    meteo.conv_Cvr('TotSkyCvr')
    meteo.conv_Cvr('OpaqSkyCvr')
    meteo.add_forFMU()
    meteo.save_csv()

    print(meteo.csv.head())