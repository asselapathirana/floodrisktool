import pandas as pd
from swmmmodel import get_depth



def strip(text):
    try:
        return text.strip()
    except AttributeError:
        return text


def read_file(path):

    df = pd.read_csv(path, delim_whitespace=True,
                      #names=["Date", "time", "level"],
                      converters = {'Date': strip, 
                      'time':strip,
                      'level':strip}
    )
    df['date'] = pd.to_datetime(df.Date+' '+df.time)
    df=df.drop(['Date', 'time'], axis=1)
    return df

def read_sealevel(path):
    df = read_file(path)
    df['Day']=df.index/24.
    df['level'] = pd.to_numeric(df['level'])
    return(df)

def read_flowFile(path2):
    df2 = pd.read_csv(path2, sep='\t')
    df2 = df2.rename(columns={"flow 1(m^3/s)": "Flow1", "flow 2(m^3/s)":"Flow2"})
    df2 = df2.drop(['time'], axis=1)
    return(df2)

def read_flow(path2):
    df2= read_flowFile(path2)
    return(df2)

def run_model(sldata, usbc1data, usbc2data):
    res = get_depth([usbc1data, usbc2data, sldata])
    # The results are ASSUMED to be hourly (Fix this later - if the model changes)
    tt = range(len(res))
    tt = [x/24.0 for x in tt]
    return [tt, res]
    

if __name__=="__main__":
    path='/Chandani/GAMING TOOL/BOUNDARY CONDITION FOR GAMING TOOL/CSV FILE/sealevels/sealevels_20010806.csv'
    path2='/Chandani\GAMING TOOL/BOUNDARY CONDITION FOR GAMING TOOL/CSV FILE/upastreamBC/Upstreambc_20000903.csv'
    df = read_sealevel(path)
    df2 = read_flow(path2)
    print('print df = ' , df.iloc[0:48])
    print('print df2 = ' , df2)
    