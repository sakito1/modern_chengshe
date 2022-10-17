class NotNumError_new(ValueError):
    def __init__(self,region, year , month,day,hour,pollutant):
        self.message=f"{pollutant:} in {region:}  on {year:} {month:} {day:} {hour:} is NULL"
        self.region=region
        self.year=year
        self.month=month
        self.day=day
        self.hour=hour
        self.pollutant=pollutant
