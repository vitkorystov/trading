from process_data.data_from_db import DataFromDataBase
from tech_analysis.indicators import Indicators
from db.data_supplier import DataSupplier


ds = DataSupplier(table='futures')
res = ds.get_data(ticker='Si-3.21')



print(res.keys())
