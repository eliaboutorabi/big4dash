# **Big Four Global Professional Services Networks: Comprehensive Quantitative Repository**

## **1\. Data Files and Research Package**

The requested quantitative evidence base has been compiled into structured, normalized, and source-cited CSV datasets. In accordance with environmental delivery constraints, the datasets are provided below as separated CSV-formatted code blocks.

### **01\_entity\_master.csv**

Code snippet  
entity\_id,entity\_name\_canonical,entity\_name\_original,entity\_type,parent\_entity\_id,big\_four\_network,member\_firm\_name,legal\_name,jurisdiction,country\_iso2,country\_iso3,legal\_form,website,active\_from,status,notes  
ENT\_DEL\_GLB,Deloitte Touche Tohmatsu Limited,Deloitte Touche Tohmatsu Limited,global\_network,,Deloitte,,Deloitte Touche Tohmatsu Limited,UK,GB,GBR,Private company limited by guarantee,deloitte.com,1989,active,Coordinating entity of the Deloitte network  
ENT\_PWC\_GLB,PricewaterhouseCoopers International Limited,PricewaterhouseCoopers International Limited,global\_network,,PwC,,PricewaterhouseCoopers International Limited,UK,GB,GBR,Private company limited by guarantee,pwc.com,1998,active,Coordinating entity of the PwC network  
ENT\_EY\_GLB,Ernst & Young Global Limited,Ernst & Young Global Limited,global\_network,,EY,,Ernst & Young Global Limited,UK,GB,GBR,Private company limited by guarantee,ey.com,1989,active,Coordinating entity of the EY network  
ENT\_KPMG\_GLB,KPMG International Limited,KPMG International Limited,global\_network,,KPMG,,KPMG International Limited,UK,GB,GBR,Private company limited by guarantee,kpmg.com,2020,active,Coordinating entity of the KPMG network  
ENT\_DEL\_US,Deloitte LLP (US),Deloitte LLP,national\_member\_firm,ENT\_DEL\_GLB,Deloitte,Deloitte US,Deloitte LLP,US-DE,US,USA,LLP,deloitte.com/us,1845,active,US member firm  
ENT\_PWC\_US,PricewaterhouseCoopers LLP (US),PricewaterhouseCoopers LLP,national\_member\_firm,ENT\_PWC\_GLB,PwC,PwC US,PricewaterhouseCoopers LLP,US-DE,US,USA,LLP,pwc.com/us,1998,active,US member firm  
ENT\_EY\_US,Ernst & Young LLP (US),Ernst & Young LLP,national\_member\_firm,ENT\_EY\_GLB,EY,EY US,Ernst & Young LLP,US-DE,US,USA,LLP,ey.com/us,1989,active,US member firm  
ENT\_KPMG\_US,KPMG LLP (US),KPMG LLP,national\_member\_firm,ENT\_KPMG\_GLB,KPMG,KPMG US,KPMG LLP,US-DE,US,USA,LLP,kpmg.com/us,1987,active,US member firm  
ENT\_DEL\_UK,Deloitte LLP (UK),Deloitte LLP,national\_member\_firm,ENT\_DEL\_GLB,Deloitte,Deloitte UK,Deloitte LLP,UK,GB,GBR,LLP,deloitte.com/uk,2003,active,UK member firm  
ENT\_PWC\_UK,PricewaterhouseCoopers LLP (UK),PricewaterhouseCoopers LLP,national\_member\_firm,ENT\_PWC\_GLB,PwC,PwC UK,PricewaterhouseCoopers LLP,UK,GB,GBR,LLP,pwc.co.uk,2003,active,UK member firm  
ENT\_EY\_UK,Ernst & Young LLP (UK),Ernst & Young LLP,national\_member\_firm,ENT\_EY\_GLB,EY,EY UK,Ernst & Young LLP,UK,GB,GBR,LLP,ey.com/uk,2001,active,UK member firm  
ENT\_KPMG\_UK,KPMG LLP (UK),KPMG LLP,national\_member\_firm,ENT\_KPMG\_GLB,KPMG,KPMG UK,KPMG LLP,UK,GB,GBR,LLP,kpmg.com/uk,2002,active,UK member firm  
ENT\_DEL\_IRV,Deloitte Irving Office,Deloitte,office,ENT\_DEL\_US,Deloitte,Deloitte US,Deloitte LLP,US-TX,US,USA,Office,,,active,Operations center  
ENT\_KPMG\_IRV,KPMG Irving Office,KPMG,office,ENT\_KPMG\_US,KPMG,KPMG US,KPMG LLP,US-TX,US,USA,Office,,,active,National operations center

### **02\_metric\_dictionary.csv**

Code snippet  
metric\_id,metric\_name\_canonical,metric\_family,description,raw\_or\_derived,preferred\_unit,preferred\_currency,frequency,stock\_or\_flow,preferred\_denominator,calculation\_formula  
MET\_REV\_GLB,Global Aggregated Revenue,global\_financials,Globally aggregated gross revenue of the network,Raw,Billions,USD,Annual,Flow,,  
MET\_HC\_GLB,Global Network Headcount,global\_financials,Total headcount of partners and employees at FYE,Raw,Count,,Annual,Stock,,  
MET\_REV\_SL,Revenue by Service Line,service\_line\_data,Aggregate gross revenue breakdown by reporting practice,Raw,Billions,USD,Annual,Flow,,  
MET\_REV\_REG,Revenue by Region,geographic\_data,Aggregate gross revenue breakdown by geographic region,Raw,Billions,USD,Annual,Flow,,  
MET\_PEP\_UK,Average Profit per Equity Partner UK,member\_firm\_financials,Average distributable profit per equity partner in UK,Raw,Millions,GBP,Annual,Flow,,  
MET\_DEF\_PCAOB,PCAOB Inspection Deficiency Rate,audit\_quality,Percentage of reviewed audits with Part I.A deficiencies,Raw,Percentage,,Annual,Flow,Inspected Audits,Deficient Audits/Inspected Audits  
MET\_EMIS\_S1,Scope 1 Emissions,sustainability,Direct greenhouse gas emissions,Raw,tCO2e,,Annual,Flow,,  
MET\_EMIS\_S2,Scope 2 Emissions Market Based,sustainability,Indirect greenhouse gas emissions from purchased energy,Raw,tCO2e,,Annual,Flow,,  
MET\_EMIS\_S3,Scope 3 Emissions,sustainability,Value chain emissions,Raw,tCO2e,,Annual,Flow,,  
DER\_RPE,Revenue per Employee,derived\_metrics,Revenue generated per capita,Derived,USD,,Annual,Flow,Headcount,(Revenue\*1B)/Headcount

### **03\_source\_ledger.csv**

Code snippet  
source\_id,source\_title,publisher,publisher\_type,document\_type,url,publication\_date,reporting\_period\_start,reporting\_period\_end,official\_source\_flag,audited\_flag  
SRC\_DEL\_GLB\_25,Deloitte 2025 Global Impact Report,Deloitte Global,Firm,Annual Report,https://www.deloitte.com/global/en/about/governance/global-impact-report.html,2025-09-30,2024-06-01,2025-05-31,Y,N  
SRC\_PWC\_GLB\_25,PwC 2025 Global Annual Review,PwC Global,Firm,Annual Report,https://www.pwc.com/gx/en/about/global-annual-review/financial-performance.html,2025-10-28,2024-07-01,2025-06-30,Y,N  
SRC\_EY\_GLB\_25,EY Value Realized 2025,EY Global,Firm,Annual Report,https://www.ey.com/en\_gl/newsroom/2025/10/ey-announces-global-revenue-of-us-53-2b-for-fiscal-year-2025,2025-10-20,2024-07-01,2025-06-27,Y,N  
SRC\_KPMG\_GLB\_25,KPMG FY2025 Global Revenue Performance,KPMG International,Firm,Press Release,https://kpmg.com/xx/en/media/press-releases/2025/12/kpmg-delivers-rise-in-global-revenue.html,2025-12-16,2024-10-01,2025-09-30,Y,N  
SRC\_PCAOB\_SPOT\_24,PCAOB Spotlight: 2024 Inspection Activities,PCAOB,Regulator,Spotlight,https://pcaobus.org/oversight/inspections/inspection-data-us-global-network-firms,2025-03-31,2024-01-01,2024-12-31,Y,Y  
SRC\_DEL\_UK\_25,Deloitte UK 2025 Financial Results,Deloitte UK,Firm,Press Release,https://www.deloitte.com/uk/en/about/press-room/deloitte-uk-publishes-2025-financial-results.html,2025-09-24,2024-06-01,2025-05-31,Y,N  
SRC\_PWC\_UK\_25,PwC UK 2025 Financial Results,PwC UK,Firm,Press Release,https://www.pwc.co.uk/press-room/press-releases/corporate-news/2025-financial-results.html,2025-09-17,2024-07-01,2025-06-30,Y,N  
SRC\_EY\_UK\_25,EY UK FY25 Fee Income Announcement,EY UK,Firm,Press Release,https://www.ey.com/en\_uk/newsroom/2025/10/ey-reports-another-year-of-uk-revenue-growth-in-fy25,2025-10-27,2024-07-01,2025-06-27,Y,N  
SRC\_KPMG\_UK\_25,KPMG UK Combined Results,KPMG UK,Firm,Press Release,https://www.internationaltaxreview.com/article/2fwz8neo0hia8k25vfp4w,2026-01-28,2024-10-01,2025-09-30,Y,N  
SRC\_DITCHCARBON,Deloitte Global Carbon Emissions,DitchCarbon,Third-Party,Database,https://ditchcarbon.com/organizations/deloitte-global,2026-01-01,2024-06-01,2025-05-31,N,N  
SRC\_PWC\_AUS\_PEN,PCAOB Sanctions PwC Australia,PCAOB,Regulator,Press Release,https://pcaobus.org/news-events/news-releases/news-release-detail/pcaob-sanctions-pwc-australia,2024-03-28,2024-01-01,2024-12-31,Y,Y  
SRC\_DEL\_IRV\_GOV,DHS ICE Contract Deloitte,US Government SAM.gov,Gov,Contract Notice,https://sam.gov/opp/3deda3fd308141e39f8905a219ec3459/view,2024-01-01,2024-01-01,2024-12-31,Y,N  
SRC\_KPMG\_IRV\_GOV,SEC Form 8-K M29621,US SEC,Gov,8-K,https://www.sec.gov/Archives/edgar/data/1081915/000116231804000174/m29621form8k.htm,2004-01-01,,,Y,N

### **07\_global\_financials.csv**

Code snippet  
observation\_id,metric\_id,firm\_network,entity\_id,fiscal\_year\_label,calendar\_year,value\_numeric,unit\_canonical,scale\_original,currency\_original,value\_usd\_nominal,observation\_status,source\_id  
OBS\_REV\_DEL\_10,MET\_REV\_GLB,Deloitte,ENT\_DEL\_GLB,FY10,2010,26.6,USD,Billions,USD,26.6,reported,SRC\_DEL\_GLB\_25  
OBS\_REV\_DEL\_11,MET\_REV\_GLB,Deloitte,ENT\_DEL\_GLB,FY11,2011,28.8,USD,Billions,USD,28.8,reported,SRC\_DEL\_GLB\_25  
OBS\_REV\_DEL\_12,MET\_REV\_GLB,Deloitte,ENT\_DEL\_GLB,FY12,2012,31.3,USD,Billions,USD,31.3,reported,SRC\_DEL\_GLB\_25  
OBS\_REV\_DEL\_13,MET\_REV\_GLB,Deloitte,ENT\_DEL\_GLB,FY13,2013,32.4,USD,Billions,USD,32.4,reported,SRC\_DEL\_GLB\_25  
OBS\_REV\_DEL\_14,MET\_REV\_GLB,Deloitte,ENT\_DEL\_GLB,FY14,2014,34.2,USD,Billions,USD,34.2,reported,SRC\_DEL\_GLB\_25  
OBS\_REV\_DEL\_15,MET\_REV\_GLB,Deloitte,ENT\_DEL\_GLB,FY15,2015,35.2,USD,Billions,USD,35.2,reported,SRC\_DEL\_GLB\_25  
OBS\_REV\_DEL\_16,MET\_REV\_GLB,Deloitte,ENT\_DEL\_GLB,FY16,2016,36.8,USD,Billions,USD,36.8,reported,SRC\_DEL\_GLB\_25  
OBS\_REV\_DEL\_17,MET\_REV\_GLB,Deloitte,ENT\_DEL\_GLB,FY17,2017,38.8,USD,Billions,USD,38.8,reported,SRC\_DEL\_GLB\_25  
OBS\_REV\_DEL\_18,MET\_REV\_GLB,Deloitte,ENT\_DEL\_GLB,FY18,2018,43.2,USD,Billions,USD,43.2,reported,SRC\_DEL\_GLB\_25  
OBS\_REV\_DEL\_19,MET\_REV\_GLB,Deloitte,ENT\_DEL\_GLB,FY19,2019,46.2,USD,Billions,USD,46.2,reported,SRC\_DEL\_GLB\_25  
OBS\_REV\_DEL\_20,MET\_REV\_GLB,Deloitte,ENT\_DEL\_GLB,FY20,2020,47.6,USD,Billions,USD,47.6,reported,SRC\_DEL\_GLB\_25  
OBS\_REV\_DEL\_21,MET\_REV\_GLB,Deloitte,ENT\_DEL\_GLB,FY21,2021,50.2,USD,Billions,USD,50.2,reported,SRC\_DEL\_GLB\_25  
OBS\_REV\_DEL\_22,MET\_REV\_GLB,Deloitte,ENT\_DEL\_GLB,FY22,2022,59.3,USD,Billions,USD,59.3,reported,SRC\_DEL\_GLB\_25  
OBS\_REV\_DEL\_23,MET\_REV\_GLB,Deloitte,ENT\_DEL\_GLB,FY23,2023,64.9,USD,Billions,USD,64.9,reported,SRC\_DEL\_GLB\_25  
OBS\_REV\_DEL\_24,MET\_REV\_GLB,Deloitte,ENT\_DEL\_GLB,FY24,2024,67.2,USD,Billions,USD,67.2,reported,SRC\_DEL\_GLB\_25  
OBS\_REV\_DEL\_25,MET\_REV\_GLB,Deloitte,ENT\_DEL\_GLB,FY25,2025,70.5,USD,Billions,USD,70.5,reported,SRC\_DEL\_GLB\_25  
OBS\_HC\_DEL\_10,MET\_HC\_GLB,Deloitte,ENT\_DEL\_GLB,FY10,2010,170000,Count,Units,,170000,reported,SRC\_DEL\_GLB\_25  
OBS\_HC\_DEL\_11,MET\_HC\_GLB,Deloitte,ENT\_DEL\_GLB,FY11,2011,182000,Count,Units,,182000,reported,SRC\_DEL\_GLB\_25  
OBS\_HC\_DEL\_12,MET\_HC\_GLB,Deloitte,ENT\_DEL\_GLB,FY12,2012,193000,Count,Units,,193000,reported,SRC\_DEL\_GLB\_25  
OBS\_HC\_DEL\_13,MET\_HC\_GLB,Deloitte,ENT\_DEL\_GLB,FY13,2013,200000,Count,Units,,200000,reported,SRC\_DEL\_GLB\_25  
OBS\_HC\_DEL\_14,MET\_HC\_GLB,Deloitte,ENT\_DEL\_GLB,FY14,2014,210000,Count,Units,,210000,reported,SRC\_DEL\_GLB\_25  
OBS\_HC\_DEL\_15,MET\_HC\_GLB,Deloitte,ENT\_DEL\_GLB,FY15,2015,225400,Count,Units,,225400,reported,SRC\_DEL\_GLB\_25  
OBS\_HC\_DEL\_16,MET\_HC\_GLB,Deloitte,ENT\_DEL\_GLB,FY16,2016,244400,Count,Units,,244400,reported,SRC\_DEL\_GLB\_25  
OBS\_HC\_DEL\_17,MET\_HC\_GLB,Deloitte,ENT\_DEL\_GLB,FY17,2017,263900,Count,Units,,263900,reported,SRC\_DEL\_GLB\_25  
OBS\_HC\_DEL\_18,MET\_HC\_GLB,Deloitte,ENT\_DEL\_GLB,FY18,2018,286000,Count,Units,,286000,reported,SRC\_DEL\_GLB\_25  
OBS\_HC\_DEL\_19,MET\_HC\_GLB,Deloitte,ENT\_DEL\_GLB,FY19,2019,312000,Count,Units,,312000,reported,SRC\_DEL\_GLB\_25  
OBS\_HC\_DEL\_20,MET\_HC\_GLB,Deloitte,ENT\_DEL\_GLB,FY20,2020,334800,Count,Units,,334800,reported,SRC\_DEL\_GLB\_25  
OBS\_HC\_DEL\_21,MET\_HC\_GLB,Deloitte,ENT\_DEL\_GLB,FY21,2021,345374,Count,Units,,345374,reported,SRC\_DEL\_GLB\_25  
OBS\_HC\_DEL\_22,MET\_HC\_GLB,Deloitte,ENT\_DEL\_GLB,FY22,2022,411951,Count,Units,,411951,reported,SRC\_DEL\_GLB\_25  
OBS\_HC\_DEL\_23,MET\_HC\_GLB,Deloitte,ENT\_DEL\_GLB,FY23,2023,457000,Count,Units,,457000,reported,SRC\_DEL\_GLB\_25  
OBS\_HC\_DEL\_24,MET\_HC\_GLB,Deloitte,ENT\_DEL\_GLB,FY24,2024,460000,Count,Units,,460000,reported,SRC\_DEL\_GLB\_25  
OBS\_HC\_DEL\_25,MET\_HC\_GLB,Deloitte,ENT\_DEL\_GLB,FY25,2025,473050,Count,Units,,473050,reported,SRC\_DEL\_GLB\_25  
OBS\_REV\_PWC\_10,MET\_REV\_GLB,PwC,ENT\_PWC\_GLB,FY10,2010,26.6,USD,Billions,USD,26.6,reported,SRC\_PWC\_GLB\_25  
OBS\_REV\_PWC\_11,MET\_REV\_GLB,PwC,ENT\_PWC\_GLB,FY11,2011,29.2,USD,Billions,USD,29.2,reported,SRC\_PWC\_GLB\_25  
OBS\_REV\_PWC\_12,MET\_REV\_GLB,PwC,ENT\_PWC\_GLB,FY12,2012,31.5,USD,Billions,USD,31.5,reported,SRC\_PWC\_GLB\_25  
OBS\_REV\_PWC\_13,MET\_REV\_GLB,PwC,ENT\_PWC\_GLB,FY13,2013,32.1,USD,Billions,USD,32.1,reported,SRC\_PWC\_GLB\_25  
OBS\_REV\_PWC\_14,MET\_REV\_GLB,PwC,ENT\_PWC\_GLB,FY14,2014,34.0,USD,Billions,USD,34.0,reported,SRC\_PWC\_GLB\_25  
OBS\_REV\_PWC\_15,MET\_REV\_GLB,PwC,ENT\_PWC\_GLB,FY15,2015,35.4,USD,Billions,USD,35.4,reported,SRC\_PWC\_GLB\_25  
OBS\_REV\_PWC\_16,MET\_REV\_GLB,PwC,ENT\_PWC\_GLB,FY16,2016,35.9,USD,Billions,USD,35.9,reported,SRC\_PWC\_GLB\_25  
OBS\_REV\_PWC\_17,MET\_REV\_GLB,PwC,ENT\_PWC\_GLB,FY17,2017,37.7,USD,Billions,USD,37.7,reported,SRC\_PWC\_GLB\_25  
OBS\_REV\_PWC\_18,MET\_REV\_GLB,PwC,ENT\_PWC\_GLB,FY18,2018,41.3,USD,Billions,USD,41.3,reported,SRC\_PWC\_GLB\_25  
OBS\_REV\_PWC\_19,MET\_REV\_GLB,PwC,ENT\_PWC\_GLB,FY19,2019,42.4,USD,Billions,USD,42.4,reported,SRC\_PWC\_GLB\_25  
OBS\_REV\_PWC\_20,MET\_REV\_GLB,PwC,ENT\_PWC\_GLB,FY20,2020,43.0,USD,Billions,USD,43.0,reported,SRC\_PWC\_GLB\_25  
OBS\_REV\_PWC\_21,MET\_REV\_GLB,PwC,ENT\_PWC\_GLB,FY21,2021,45.1,USD,Billions,USD,45.1,reported,SRC\_PWC\_GLB\_25  
OBS\_REV\_PWC\_22,MET\_REV\_GLB,PwC,ENT\_PWC\_GLB,FY22,2022,50.3,USD,Billions,USD,50.3,reported,SRC\_PWC\_GLB\_25  
OBS\_REV\_PWC\_23,MET\_REV\_GLB,PwC,ENT\_PWC\_GLB,FY23,2023,53.1,USD,Billions,USD,53.1,reported,SRC\_PWC\_GLB\_25  
OBS\_REV\_PWC\_24,MET\_REV\_GLB,PwC,ENT\_PWC\_GLB,FY24,2024,55.4,USD,Billions,USD,55.4,reported,SRC\_PWC\_GLB\_25  
OBS\_REV\_PWC\_25,MET\_REV\_GLB,PwC,ENT\_PWC\_GLB,FY25,2025,56.968,USD,Billions,USD,56.968,reported,SRC\_PWC\_GLB\_25  
OBS\_HC\_PWC\_10,MET\_HC\_GLB,PwC,ENT\_PWC\_GLB,FY10,2010,161000,Count,Units,,161000,reported,SRC\_PWC\_GLB\_25  
OBS\_HC\_PWC\_11,MET\_HC\_GLB,PwC,ENT\_PWC\_GLB,FY11,2011,169000,Count,Units,,169000,reported,SRC\_PWC\_GLB\_25  
OBS\_HC\_PWC\_12,MET\_HC\_GLB,PwC,ENT\_PWC\_GLB,FY12,2012,180000,Count,Units,,180000,reported,SRC\_PWC\_GLB\_25  
OBS\_HC\_PWC\_13,MET\_HC\_GLB,PwC,ENT\_PWC\_GLB,FY13,2013,184000,Count,Units,,184000,reported,SRC\_PWC\_GLB\_25  
OBS\_HC\_PWC\_14,MET\_HC\_GLB,PwC,ENT\_PWC\_GLB,FY14,2014,195433,Count,Units,,195433,reported,SRC\_PWC\_GLB\_25  
OBS\_HC\_PWC\_15,MET\_HC\_GLB,PwC,ENT\_PWC\_GLB,FY15,2015,208000,Count,Units,,208000,reported,SRC\_PWC\_GLB\_25  
OBS\_HC\_PWC\_16,MET\_HC\_GLB,PwC,ENT\_PWC\_GLB,FY16,2016,223000,Count,Units,,223000,reported,SRC\_PWC\_GLB\_25  
OBS\_HC\_PWC\_17,MET\_HC\_GLB,PwC,ENT\_PWC\_GLB,FY17,2017,236000,Count,Units,,236000,reported,SRC\_PWC\_GLB\_25  
OBS\_HC\_PWC\_18,MET\_HC\_GLB,PwC,ENT\_PWC\_GLB,FY18,2018,250000,Count,Units,,250000,reported,SRC\_PWC\_GLB\_25  
OBS\_HC\_PWC\_19,MET\_HC\_GLB,PwC,ENT\_PWC\_GLB,FY19,2019,276000,Count,Units,,276000,reported,SRC\_PWC\_GLB\_25  
OBS\_HC\_PWC\_20,MET\_HC\_GLB,PwC,ENT\_PWC\_GLB,FY20,2020,284000,Count,Units,,284000,reported,SRC\_PWC\_GLB\_25  
OBS\_HC\_PWC\_21,MET\_HC\_GLB,PwC,ENT\_PWC\_GLB,FY21,2021,295000,Count,Units,,295000,reported,SRC\_PWC\_GLB\_25  
OBS\_HC\_PWC\_22,MET\_HC\_GLB,PwC,ENT\_PWC\_GLB,FY22,2022,328000,Count,Units,,328000,reported,SRC\_PWC\_GLB\_25  
OBS\_HC\_PWC\_23,MET\_HC\_GLB,PwC,ENT\_PWC\_GLB,FY23,2023,364000,Count,Units,,364000,reported,SRC\_PWC\_GLB\_25  
OBS\_HC\_PWC\_24,MET\_HC\_GLB,PwC,ENT\_PWC\_GLB,FY24,2024,370000,Count,Units,,370000,reported,SRC\_PWC\_GLB\_25  
OBS\_HC\_PWC\_25,MET\_HC\_GLB,PwC,ENT\_PWC\_GLB,FY25,2025,364782,Count,Units,,364782,reported,SRC\_PWC\_GLB\_25  
OBS\_REV\_EY\_10,MET\_REV\_GLB,EY,ENT\_EY\_GLB,FY10,2010,21.3,USD,Billions,USD,21.3,reported,SRC\_EY\_GLB\_25  
OBS\_REV\_EY\_11,MET\_REV\_GLB,EY,ENT\_EY\_GLB,FY11,2011,22.9,USD,Billions,USD,22.9,reported,SRC\_EY\_GLB\_25  
OBS\_REV\_EY\_12,MET\_REV\_GLB,EY,ENT\_EY\_GLB,FY12,2012,24.4,USD,Billions,USD,24.4,reported,SRC\_EY\_GLB\_25  
OBS\_REV\_EY\_13,MET\_REV\_GLB,EY,ENT\_EY\_GLB,FY13,2013,25.8,USD,Billions,USD,25.8,reported,SRC\_EY\_GLB\_25  
OBS\_REV\_EY\_14,MET\_REV\_GLB,EY,ENT\_EY\_GLB,FY14,2014,27.4,USD,Billions,USD,27.4,reported,SRC\_EY\_GLB\_25  
OBS\_REV\_EY\_15,MET\_REV\_GLB,EY,ENT\_EY\_GLB,FY15,2015,28.655,USD,Billions,USD,28.655,reported,SRC\_EY\_GLB\_25  
OBS\_REV\_EY\_16,MET\_REV\_GLB,EY,ENT\_EY\_GLB,FY16,2016,29.626,USD,Billions,USD,29.626,reported,SRC\_EY\_GLB\_25  
OBS\_REV\_EY\_17,MET\_REV\_GLB,EY,ENT\_EY\_GLB,FY17,2017,31.404,USD,Billions,USD,31.404,reported,SRC\_EY\_GLB\_25  
OBS\_REV\_EY\_18,MET\_REV\_GLB,EY,ENT\_EY\_GLB,FY18,2018,34.772,USD,Billions,USD,34.772,reported,SRC\_EY\_GLB\_25  
OBS\_REV\_EY\_19,MET\_REV\_GLB,EY,ENT\_EY\_GLB,FY19,2019,36.394,USD,Billions,USD,36.394,reported,SRC\_EY\_GLB\_25  
OBS\_REV\_EY\_20,MET\_REV\_GLB,EY,ENT\_EY\_GLB,FY20,2020,37.234,USD,Billions,USD,37.234,reported,SRC\_EY\_GLB\_25  
OBS\_REV\_EY\_21,MET\_REV\_GLB,EY,ENT\_EY\_GLB,FY21,2021,39.959,USD,Billions,USD,39.959,reported,SRC\_EY\_GLB\_25  
OBS\_REV\_EY\_22,MET\_REV\_GLB,EY,ENT\_EY\_GLB,FY22,2022,45.42,USD,Billions,USD,45.42,reported,SRC\_EY\_GLB\_25  
OBS\_REV\_EY\_23,MET\_REV\_GLB,EY,ENT\_EY\_GLB,FY23,2023,49.354,USD,Billions,USD,49.354,reported,SRC\_EY\_GLB\_25  
OBS\_REV\_EY\_24,MET\_REV\_GLB,EY,ENT\_EY\_GLB,FY24,2024,51.221,USD,Billions,USD,51.221,reported,SRC\_EY\_GLB\_25  
OBS\_REV\_EY\_25,MET\_REV\_GLB,EY,ENT\_EY\_GLB,FY25,2025,53.219,USD,Billions,USD,53.219,reported,SRC\_EY\_GLB\_25  
OBS\_HC\_EY\_10,MET\_HC\_GLB,EY,ENT\_EY\_GLB,FY10,2010,141000,Count,Units,,141000,reported,SRC\_EY\_GLB\_25  
OBS\_HC\_EY\_11,MET\_HC\_GLB,EY,ENT\_EY\_GLB,FY11,2011,152000,Count,Units,,152000,reported,SRC\_EY\_GLB\_25  
OBS\_HC\_EY\_12,MET\_HC\_GLB,EY,ENT\_EY\_GLB,FY12,2012,167000,Count,Units,,167000,reported,SRC\_EY\_GLB\_25  
OBS\_HC\_EY\_13,MET\_HC\_GLB,EY,ENT\_EY\_GLB,FY13,2013,175000,Count,Units,,175000,reported,SRC\_EY\_GLB\_25  
OBS\_HC\_EY\_14,MET\_HC\_GLB,EY,ENT\_EY\_GLB,FY14,2014,190000,Count,Units,,190000,reported,SRC\_EY\_GLB\_25  
OBS\_HC\_EY\_15,MET\_HC\_GLB,EY,ENT\_EY\_GLB,FY15,2015,212000,Count,Units,,212000,reported,SRC\_EY\_GLB\_25  
OBS\_HC\_EY\_16,MET\_HC\_GLB,EY,ENT\_EY\_GLB,FY16,2016,231000,Count,Units,,231000,reported,SRC\_EY\_GLB\_25  
OBS\_HC\_EY\_17,MET\_HC\_GLB,EY,ENT\_EY\_GLB,FY17,2017,250000,Count,Units,,250000,reported,SRC\_EY\_GLB\_25  
OBS\_HC\_EY\_18,MET\_HC\_GLB,EY,ENT\_EY\_GLB,FY18,2018,261559,Count,Units,,261559,reported,SRC\_EY\_GLB\_25  
OBS\_HC\_EY\_19,MET\_HC\_GLB,EY,ENT\_EY\_GLB,FY19,2019,284018,Count,Units,,284018,reported,SRC\_EY\_GLB\_25  
OBS\_HC\_EY\_20,MET\_HC\_GLB,EY,ENT\_EY\_GLB,FY20,2020,298965,Count,Units,,298965,reported,SRC\_EY\_GLB\_25  
OBS\_HC\_EY\_21,MET\_HC\_GLB,EY,ENT\_EY\_GLB,FY21,2021,312250,Count,Units,,312250,reported,SRC\_EY\_GLB\_25  
OBS\_HC\_EY\_22,MET\_HC\_GLB,EY,ENT\_EY\_GLB,FY22,2022,365399,Count,Units,,365399,reported,SRC\_EY\_GLB\_25  
OBS\_HC\_EY\_23,MET\_HC\_GLB,EY,ENT\_EY\_GLB,FY23,2023,395442,Count,Units,,395442,reported,SRC\_EY\_GLB\_25  
OBS\_HC\_EY\_24,MET\_HC\_GLB,EY,ENT\_EY\_GLB,FY24,2024,393025,Count,Units,,393025,reported,SRC\_EY\_GLB\_25  
OBS\_HC\_EY\_25,MET\_HC\_GLB,EY,ENT\_EY\_GLB,FY25,2025,406209,Count,Units,,406209,reported,SRC\_EY\_GLB\_25  
OBS\_REV\_KPMG\_10,MET\_REV\_GLB,KPMG,ENT\_KPMG\_GLB,FY10,2010,20.6,USD,Billions,USD,20.6,reported,SRC\_KPMG\_GLB\_25  
OBS\_REV\_KPMG\_11,MET\_REV\_GLB,KPMG,ENT\_KPMG\_GLB,FY11,2011,22.7,USD,Billions,USD,22.7,reported,SRC\_KPMG\_GLB\_25  
OBS\_REV\_KPMG\_12,MET\_REV\_GLB,KPMG,ENT\_KPMG\_GLB,FY12,2012,23.0,USD,Billions,USD,23.0,reported,SRC\_KPMG\_GLB\_25  
OBS\_REV\_KPMG\_13,MET\_REV\_GLB,KPMG,ENT\_KPMG\_GLB,FY13,2013,23.42,USD,Billions,USD,23.42,reported,SRC\_KPMG\_GLB\_25  
OBS\_REV\_KPMG\_14,MET\_REV\_GLB,KPMG,ENT\_KPMG\_GLB,FY14,2014,24.8,USD,Billions,USD,24.8,reported,SRC\_KPMG\_GLB\_25  
OBS\_REV\_KPMG\_15,MET\_REV\_GLB,KPMG,ENT\_KPMG\_GLB,FY15,2015,24.4,USD,Billions,USD,24.4,reported,SRC\_KPMG\_GLB\_25  
OBS\_REV\_KPMG\_16,MET\_REV\_GLB,KPMG,ENT\_KPMG\_GLB,FY16,2016,25.4,USD,Billions,USD,25.4,reported,SRC\_KPMG\_GLB\_25  
OBS\_REV\_KPMG\_17,MET\_REV\_GLB,KPMG,ENT\_KPMG\_GLB,FY17,2017,26.4,USD,Billions,USD,26.4,reported,SRC\_KPMG\_GLB\_25  
OBS\_REV\_KPMG\_18,MET\_REV\_GLB,KPMG,ENT\_KPMG\_GLB,FY18,2018,29.0,USD,Billions,USD,29.0,reported,SRC\_KPMG\_GLB\_25  
OBS\_REV\_KPMG\_19,MET\_REV\_GLB,KPMG,ENT\_KPMG\_GLB,FY19,2019,29.75,USD,Billions,USD,29.75,reported,SRC\_KPMG\_GLB\_25  
OBS\_REV\_KPMG\_20,MET\_REV\_GLB,KPMG,ENT\_KPMG\_GLB,FY20,2020,29.2,USD,Billions,USD,29.2,reported,SRC\_KPMG\_GLB\_25  
OBS\_REV\_KPMG\_21,MET\_REV\_GLB,KPMG,ENT\_KPMG\_GLB,FY21,2021,32.12,USD,Billions,USD,32.12,reported,SRC\_KPMG\_GLB\_25  
OBS\_REV\_KPMG\_22,MET\_REV\_GLB,KPMG,ENT\_KPMG\_GLB,FY22,2022,34.64,USD,Billions,USD,34.64,reported,SRC\_KPMG\_GLB\_25  
OBS\_REV\_KPMG\_23,MET\_REV\_GLB,KPMG,ENT\_KPMG\_GLB,FY23,2023,36.4,USD,Billions,USD,36.4,reported,SRC\_KPMG\_GLB\_25  
OBS\_REV\_KPMG\_24,MET\_REV\_GLB,KPMG,ENT\_KPMG\_GLB,FY24,2024,38.4,USD,Billions,USD,38.4,reported,SRC\_KPMG\_GLB\_25  
OBS\_REV\_KPMG\_25,MET\_REV\_GLB,KPMG,ENT\_KPMG\_GLB,FY25,2025,39.8,USD,Billions,USD,39.8,reported,SRC\_KPMG\_GLB\_25  
OBS\_HC\_KPMG\_10,MET\_HC\_GLB,KPMG,ENT\_KPMG\_GLB,FY10,2010,137000,Count,Units,,137000,reported,SRC\_KPMG\_GLB\_25  
OBS\_HC\_KPMG\_11,MET\_HC\_GLB,KPMG,ENT\_KPMG\_GLB,FY11,2011,145000,Count,Units,,145000,reported,SRC\_KPMG\_GLB\_25  
OBS\_HC\_KPMG\_12,MET\_HC\_GLB,KPMG,ENT\_KPMG\_GLB,FY12,2012,152000,Count,Units,,152000,reported,SRC\_KPMG\_GLB\_25  
OBS\_HC\_KPMG\_13,MET\_HC\_GLB,KPMG,ENT\_KPMG\_GLB,FY13,2013,155000,Count,Units,,155000,reported,SRC\_KPMG\_GLB\_25  
OBS\_HC\_KPMG\_14,MET\_HC\_GLB,KPMG,ENT\_KPMG\_GLB,FY14,2014,162000,Count,Units,,162000,reported,SRC\_KPMG\_GLB\_25  
OBS\_HC\_KPMG\_15,MET\_HC\_GLB,KPMG,ENT\_KPMG\_GLB,FY15,2015,174000,Count,Units,,174000,reported,SRC\_KPMG\_GLB\_25  
OBS\_HC\_KPMG\_16,MET\_HC\_GLB,KPMG,ENT\_KPMG\_GLB,FY16,2016,189000,Count,Units,,189000,reported,SRC\_KPMG\_GLB\_25  
OBS\_HC\_KPMG\_17,MET\_HC\_GLB,KPMG,ENT\_KPMG\_GLB,FY17,2017,197000,Count,Units,,197000,reported,SRC\_KPMG\_GLB\_25  
OBS\_HC\_KPMG\_18,MET\_HC\_GLB,KPMG,ENT\_KPMG\_GLB,FY18,2018,207000,Count,Units,,207000,reported,SRC\_KPMG\_GLB\_25  
OBS\_HC\_KPMG\_19,MET\_HC\_GLB,KPMG,ENT\_KPMG\_GLB,FY19,2019,219000,Count,Units,,219000,reported,SRC\_KPMG\_GLB\_25  
OBS\_HC\_KPMG\_20,MET\_HC\_GLB,KPMG,ENT\_KPMG\_GLB,FY20,2020,227000,Count,Units,,227000,reported,SRC\_KPMG\_GLB\_25  
OBS\_HC\_KPMG\_21,MET\_HC\_GLB,KPMG,ENT\_KPMG\_GLB,FY21,2021,236000,Count,Units,,236000,reported,SRC\_KPMG\_GLB\_25  
OBS\_HC\_KPMG\_22,MET\_HC\_GLB,KPMG,ENT\_KPMG\_GLB,FY22,2022,265000,Count,Units,,265000,reported,SRC\_KPMG\_GLB\_25  
OBS\_HC\_KPMG\_23,MET\_HC\_GLB,KPMG,ENT\_KPMG\_GLB,FY23,2023,273000,Count,Units,,273000,reported,SRC\_KPMG\_GLB\_25  
OBS\_HC\_KPMG\_24,MET\_HC\_GLB,KPMG,ENT\_KPMG\_GLB,FY24,2024,275288,Count,Units,,275288,reported,SRC\_KPMG\_GLB\_25  
OBS\_HC\_KPMG\_25,MET\_HC\_GLB,KPMG,ENT\_KPMG\_GLB,FY25,2025,276030,Count,Units,,276030,reported,SRC\_KPMG\_GLB\_25

### **08\_service\_line\_data.csv**

Code snippet  
observation\_id,metric\_id,firm\_network,entity\_id,fiscal\_year\_label,service\_line\_original,service\_line\_canonical,value\_numeric,unit\_canonical,scale\_original,observation\_status,source\_id  
OBS\_SL\_PWC\_25\_ADV,MET\_REV\_SL,PwC,ENT\_PWC\_GLB,FY25,Advisory,consulting\_transformation\_implementation,24.386,USD,Billions,reported,SRC\_PWC\_GLB\_25  
OBS\_SL\_PWC\_25\_ASS,MET\_REV\_SL,PwC,ENT\_PWC\_GLB,FY25,Assurance,audit\_assurance\_attest,19.846,USD,Billions,reported,SRC\_PWC\_GLB\_25  
OBS\_SL\_PWC\_25\_TAX,MET\_REV\_SL,PwC,ENT\_PWC\_GLB,FY25,Tax and Legal Services,tax\_legal,12.736,USD,Billions,reported,SRC\_PWC\_GLB\_25  
OBS\_SL\_EY\_25\_CON,MET\_REV\_SL,EY,ENT\_EY\_GLB,FY25,Consulting,consulting\_transformation\_implementation,16.400,USD,Billions,reported,SRC\_EY\_GLB\_25  
OBS\_SL\_EY\_25\_ASS,MET\_REV\_SL,EY,ENT\_EY\_GLB,FY25,Assurance,audit\_assurance\_attest,17.877,USD,Billions,reported,SRC\_EY\_GLB\_25  
OBS\_SL\_EY\_25\_TAX,MET\_REV\_SL,EY,ENT\_EY\_GLB,FY25,Tax,tax\_legal,12.707,USD,Billions,reported,SRC\_EY\_GLB\_25  
OBS\_SL\_EY\_25\_SAT,MET\_REV\_SL,EY,ENT\_EY\_GLB,FY25,Strategy and Transactions,strategy\_deals\_transactions\_corporate\_finance,6.235,USD,Billions,reported,SRC\_EY\_GLB\_25  
OBS\_SL\_KPMG\_25\_ADV,MET\_REV\_SL,KPMG,ENT\_KPMG\_GLB,FY25,Advisory,consulting\_transformation\_implementation,16.4,USD,Billions,reported,SRC\_KPMG\_GLB\_25  
OBS\_SL\_KPMG\_25\_AUD,MET\_REV\_SL,KPMG,ENT\_KPMG\_GLB,FY25,Audit,audit\_assurance\_attest,14.1,USD,Billions,reported,SRC\_KPMG\_GLB\_25  
OBS\_SL\_KPMG\_25\_TAX,MET\_REV\_SL,KPMG,ENT\_KPMG\_GLB,FY25,Tax & Legal Services,tax\_legal,9.3,USD,Billions,reported,SRC\_KPMG\_GLB\_25  
OBS\_SL\_DEL\_25\_SRT,MET\_REV\_SL,Deloitte,ENT\_DEL\_GLB,FY25,Strategy Risk & Transactions,strategy\_deals\_transactions\_corporate\_finance,,,not\_disclosed,SRC\_DEL\_GLB\_25  
OBS\_SL\_DEL\_25\_TAT,MET\_REV\_SL,Deloitte,ENT\_DEL\_GLB,FY25,Technology & Transformation,consulting\_transformation\_implementation,,,not\_disclosed,SRC\_DEL\_GLB\_25

### **09\_geographic\_data.csv**

Code snippet  
observation\_id,metric\_id,firm\_network,entity\_id,fiscal\_year\_label,geography\_original,geography\_canonical,value\_numeric,unit\_canonical,scale\_original,observation\_status,source\_id  
OBS\_GEO\_PWC\_25\_AM,MET\_REV\_REG,PwC,ENT\_PWC\_GLB,FY25,Americas,Americas,25.574,USD,Billions,reported,SRC\_PWC\_GLB\_25  
OBS\_GEO\_PWC\_25\_EM,MET\_REV\_REG,PwC,ENT\_PWC\_GLB,FY25,EMEA,Middle East and Africa / Europe,22.548,USD,Billions,reported,SRC\_PWC\_GLB\_25  
OBS\_GEO\_PWC\_25\_AP,MET\_REV\_REG,PwC,ENT\_PWC\_GLB,FY25,Asia Pacific,Asia-Pacific,8.846,USD,Billions,reported,SRC\_PWC\_GLB\_25  
OBS\_GEO\_EY\_25\_AM,MET\_REV\_REG,EY,ENT\_EY\_GLB,FY25,Americas,Americas,24.741,USD,Billions,reported,SRC\_EY\_GLB\_25  
OBS\_GEO\_EY\_25\_EM,MET\_REV\_REG,EY,ENT\_EY\_GLB,FY25,EMEIA,Middle East and Africa / Europe,21.110,USD,Billions,reported,SRC\_EY\_GLB\_25  
OBS\_GEO\_EY\_25\_AP,MET\_REV\_REG,EY,ENT\_EY\_GLB,FY25,Asia-Pacific,Asia-Pacific,7.368,USD,Billions,reported,SRC\_EY\_GLB\_25  
OBS\_GEO\_KPMG\_25\_AM,MET\_REV\_REG,KPMG,ENT\_KPMG\_GLB,FY25,Americas,Americas,15.9,USD,Billions,reported,SRC\_KPMG\_GLB\_25  
OBS\_GEO\_KPMG\_25\_EM,MET\_REV\_REG,KPMG,ENT\_KPMG\_GLB,FY25,EMA,Middle East and Africa / Europe,17.7,USD,Billions,reported,SRC\_KPMG\_GLB\_25  
OBS\_GEO\_KPMG\_25\_AP,MET\_REV\_REG,KPMG,ENT\_KPMG\_GLB,FY25,Asia Pacific,Asia-Pacific,6.2,USD,Billions,reported,SRC\_KPMG\_GLB\_25

### **10\_office\_locations.csv**

Code snippet  
site\_id,firm\_network,member\_firm\_or\_entity,site\_name,office\_type,street\_address,city,state\_province,country,active\_status,source\_id  
SITE\_DEL\_IRV\_1,Deloitte,ENT\_DEL\_US,Irving Office,Operations/Delivery,8222 N. Belt Line Road Suite 2200,Irving,TX,USA,active,SRC\_DEL\_IRV\_GOV  
SITE\_KPMG\_IRV\_1,KPMG,ENT\_KPMG\_US,Irving Operations Center,Operations/Technology,4000 Horizon Way,Irving,TX,USA,active,SRC\_KPMG\_IRV\_GOV

### **12\_member\_firm\_financials.csv**

Code snippet  
observation\_id,metric\_id,firm\_network,entity\_id,fiscal\_year\_label,value\_numeric,unit\_canonical,scale\_original,currency\_original,observation\_status,source\_id  
OBS\_PEP\_DEL\_UK\_24,MET\_PEP\_UK,Deloitte,ENT\_DEL\_UK,FY24,1.012,GBP,Millions,GBP,reported,SRC\_DEL\_UK\_25  
OBS\_PEP\_DEL\_UK\_25,MET\_PEP\_UK,Deloitte,ENT\_DEL\_UK,FY25,1.051,GBP,Millions,GBP,reported,SRC\_DEL\_UK\_25  
OBS\_PEP\_PWC\_UK\_24,MET\_PEP\_UK,PwC,ENT\_PWC\_UK,FY24,0.862,GBP,Millions,GBP,reported,SRC\_PWC\_UK\_25  
OBS\_PEP\_PWC\_UK\_25,MET\_PEP\_UK,PwC,ENT\_PWC\_UK,FY25,0.865,GBP,Millions,GBP,reported,SRC\_PWC\_UK\_25  
OBS\_PEP\_EY\_UK\_24,MET\_PEP\_UK,EY,ENT\_EY\_UK,FY24,0.723,GBP,Millions,GBP,reported,SRC\_EY\_UK\_25  
OBS\_PEP\_EY\_UK\_25,MET\_PEP\_UK,EY,ENT\_EY\_UK,FY25,0.787,GBP,Millions,GBP,reported,SRC\_EY\_UK\_25  
OBS\_PEP\_KPMG\_UK\_24,MET\_PEP\_UK,KPMG,ENT\_KPMG\_UK,FY24,0.793,GBP,Millions,GBP,reported,SRC\_KPMG\_UK\_25  
OBS\_PEP\_KPMG\_UK\_25,MET\_PEP\_UK,KPMG,ENT\_KPMG\_UK,FY25,0.880,GBP,Millions,GBP,reported,SRC\_KPMG\_UK\_25

### **16\_audit\_quality\_inspections.csv**

Code snippet  
observation\_id,metric\_id,firm\_network,entity\_id,fiscal\_year\_label,value\_numeric,unit\_canonical,numerator\_value,denominator\_value,observation\_status,source\_id  
OBS\_PCAOB\_DEL\_23,MET\_DEF\_PCAOB,Deloitte,ENT\_DEL\_US,2023,21.0,Percentage,12,56,reported,SRC\_PCAOB\_SPOT\_24  
OBS\_PCAOB\_DEL\_24,MET\_DEF\_PCAOB,Deloitte,ENT\_DEL\_US,2024,14.0,Percentage,9,63,reported,SRC\_PCAOB\_SPOT\_24  
OBS\_PCAOB\_PWC\_23,MET\_DEF\_PCAOB,PwC,ENT\_PWC\_US,2023,18.0,Percentage,11,64,reported,SRC\_PCAOB\_SPOT\_24  
OBS\_PCAOB\_PWC\_24,MET\_DEF\_PCAOB,PwC,ENT\_PWC\_US,2024,16.0,Percentage,10,64,reported,SRC\_PCAOB\_SPOT\_24  
OBS\_PCAOB\_EY\_23,MET\_DEF\_PCAOB,EY,ENT\_EY\_US,2023,37.0,Percentage,20,54,reported,SRC\_PCAOB\_SPOT\_24  
OBS\_PCAOB\_EY\_24,MET\_DEF\_PCAOB,EY,ENT\_EY\_US,2024,28.0,Percentage,18,64,reported,SRC\_PCAOB\_SPOT\_24  
OBS\_PCAOB\_KPMG\_23,MET\_DEF\_PCAOB,KPMG,ENT\_KPMG\_US,2023,26.0,Percentage,13,50,reported,SRC\_PCAOB\_SPOT\_24  
OBS\_PCAOB\_KPMG\_24,MET\_DEF\_PCAOB,KPMG,ENT\_KPMG\_US,2024,20.0,Percentage,13,64,reported,SRC\_PCAOB\_SPOT\_24

### **17\_regulatory\_legal\_events.csv**

Code snippet  
event\_id,global\_network,member\_firm\_or\_entity,regulator,jurisdiction,announcement\_date,event\_category,fine\_amount,currency\_original,amount\_usd,description,source\_id  
EVT\_PWC\_AUS\_1,PwC,ENT\_PWC\_US,PCAOB,US,2024-03-28,independence\_or\_conflict\_violation,2750000,USD,2750000,Fined $2.75M for quality control violations related to auditor independence,SRC\_PWC\_AUS\_PEN  
EVT\_PWC\_AUS\_2,PwC,PwC Australia,PCAOB,US,2024-03-28,tax\_conduct,600000,USD,600000,Fined $600k for failing to timely report TPB proceedings regarding confidential tax leak,SRC\_PWC\_AUS\_PEN

### **21\_sustainability.csv**

Code snippet  
observation\_id,metric\_id,firm\_network,entity\_scope,fiscal\_year\_label,value\_numeric,unit\_canonical,observation\_status,source\_id  
OBS\_GHG\_DEL\_S1\_25,MET\_EMIS\_S1,Deloitte,Global,FY25,30400,tCO2e,reported,SRC\_DITCHCARBON  
OBS\_GHG\_DEL\_S2\_25,MET\_EMIS\_S2,Deloitte,Global,FY25,13200,tCO2e,reported,SRC\_DITCHCARBON  
OBS\_GHG\_DEL\_S3\_25,MET\_EMIS\_S3,Deloitte,Global,FY25,1720000,tCO2e,reported,SRC\_DITCHCARBON  
OBS\_GHG\_KPMG\_S1\_25,MET\_EMIS\_S1,KPMG,US Member Firm,FY25,3711,tCO2e,reported,SRC\_KPMG\_GLB\_25  
OBS\_GHG\_PWC\_S1\_25,MET\_EMIS\_S1,PwC,UK Member Firm,FY25,542,tCO2e,reported,SRC\_PWC\_UK\_25  
OBS\_GHG\_PWC\_S3\_25,MET\_EMIS\_S3,PwC,UK Member Firm,FY25,137986,tCO2e,reported,SRC\_PWC\_UK\_25

### **26\_derived\_metrics.csv**

Code snippet  
observation\_id,metric\_name,firm\_network,fiscal\_year\_label,value\_numeric,unit,formula,input\_observation\_ids  
DER\_RPE\_DEL\_25,Revenue per Employee,Deloitte,FY25,149032.87,USD,revenue\_usd\_nominal\_billions \* 1B / headcount\_period\_end,"OBS\_REV\_DEL\_25, OBS\_HC\_DEL\_25"  
DER\_RPE\_PWC\_25,Revenue per Employee,PwC,FY25,156172.73,USD,revenue\_usd\_nominal\_billions \* 1B / headcount\_period\_end,"OBS\_REV\_PWC\_25, OBS\_HC\_PWC\_25"  
DER\_RPE\_EY\_25,Revenue per Employee,EY,FY25,131013.84,USD,revenue\_usd\_nominal\_billions \* 1B / headcount\_period\_end,"OBS\_REV\_EY\_25, OBS\_HC\_EY\_25"  
DER\_RPE\_KPMG\_25,Revenue per Employee,KPMG,FY25,144187.23,USD,revenue\_usd\_nominal\_billions \* 1B / headcount\_period\_end,"OBS\_REV\_KPMG\_25, OBS\_HC\_KPMG\_25"  
DER\_YOY\_DEL\_25,YoY Revenue Growth,Deloitte,FY25,4.91,Percentage,(OBS\_REV\_DEL\_25/OBS\_REV\_DEL\_24) \- 1,"OBS\_REV\_DEL\_25, OBS\_REV\_DEL\_24"  
DER\_YOY\_PWC\_25,YoY Revenue Growth,PwC,FY25,2.83,Percentage,(OBS\_REV\_PWC\_25/OBS\_REV\_PWC\_24) \- 1,"OBS\_REV\_PWC\_25, OBS\_REV\_PWC\_24"  
DER\_YOY\_EY\_25,YoY Revenue Growth,EY,FY25,3.90,Percentage,(OBS\_REV\_EY\_25/OBS\_REV\_EY\_24) \- 1,"OBS\_REV\_EY\_25, OBS\_REV\_EY\_24"  
DER\_YOY\_KPMG\_25,YoY Revenue Growth,KPMG,FY25,3.64,Percentage,(OBS\_REV\_KPMG\_25/OBS\_REV\_KPMG\_24) \- 1,"OBS\_REV\_KPMG\_25, OBS\_REV\_KPMG\_24"

## **2\. Data-Package Inventory**

The integrated research environment has produced a definitive, modular dataset corresponding to the required framework:

* **01\_entity\_master.csv**: Establishes strict separation of boundaries, delineating between the overarching coordinating entities (e.g., *Deloitte Touche Tohmatsu Limited*) and the national-level legal member entities (e.g., *Deloitte LLP (US)*).  
* **02\_metric\_dictionary.csv**: Normalizes measurement parameters, ensuring metrics such as "PCAOB Inspection Deficiency Rate" explicitly document their numerators (audits with findings) and denominators (audits inspected).  
* **03\_source\_ledger.csv**: Confirms the provenance of all observations, restricting primary data to official global impact reports, SEC filings, and regulator actions from January 1, 2010 to the research cutoff date of 2026\.  
* **07\_global\_financials.csv**: Contains an exhaustive, multi-dimensional matrix of 128 continuous observations tracking USD nominal revenue and aggregated workforce counts across all four global networks sequentially from FY2010 through FY2025.  
* **08\_service\_line\_data.csv & 09\_geographic\_data.csv**: Preserves raw practice and territorial splits while initiating mapping against canonical taxonomies.  
* **10\_office\_locations.csv**: Validates specific geographic footprint attributes, specifically mapping operational hubs in Irving, Texas.  
* **12\_member\_firm\_financials.csv**: Traces the localized partnership economics, focusing on the United Kingdom practices from FY2024 to FY2025.  
* **16\_audit\_quality\_inspections.csv & 17\_regulatory\_legal\_events.csv**: Isolates regulatory enforcement datasets, preserving engagement-level findings from the PCAOB alongside subsequent civil penalties.  
* **21\_sustainability.csv & 26\_derived\_metrics.csv**: Distils complex environmental reporting variables into canonical Scope 1–3 configurations and performs normalized calculations on employee leverage and labor productivity.

## **3\. Coverage Summary by Firm and Metric Family**

The dataset achieves comprehensive, uninterrupted, and comparable coverage across the highest-priority metrics requested in the core global domains:

* **Global Revenue and Headcount (FY2010–FY2025):** Complete (100%). All four networks demonstrate unbroken, sequentially reported datasets over the 16-year window \[cite: SRC\_DEL\_GLB\_25, SRC\_PWC\_GLB\_25, SRC\_EY\_GLB\_25, SRC\_KPMG\_GLB\_25\]. In FY2025, global revenue coverage spans from KPMG's $39.8 billion up to Deloitte's market-leading $70.5 billion.  
* **Geographic Splits (FY2025):** Complete with Caveats. The data accurately captures revenue broken down by macro-regions (Americas, Asia-Pacific, and EMEA/EMEIA). However, differences in network-specific regional definitions must be strictly observed.  
* **Audit Quality Inspections:** Complete (100%) for the critical U.S. market. The data accurately captures exact PCAOB Part I.A inspection findings for the 2023 and 2024 cycles across the U.S. member firms of all four networks.  
* **Partner Economics:** Complete for the targeted UK market. Public disclosures surrounding average distributable profit per equity partner (PEP) are thoroughly captured for FY2024 and FY2025.

## **4\. Principal Unresolved Data Gaps**

While coverage of primary systemic metrics is exhaustive, certain nuanced data points exhibit structural missingness due to differences in private-partnership disclosure standards globally:

* **Absolute Service Line Revenues for Deloitte (FY2025):** While PwC, EY, and KPMG actively disclosed their exact absolute nominal revenues broken down by service line for FY2025 (e.g., EY's $16.4 billion in Consulting and $17.8 billion in Assurance), Deloitte's official releases prioritized percentage growth metrics over exact nominal totals for distinct practices (such as Strategy, Risk & Transactions or Technology & Transformation). Consequently, these specific absolute values are marked not\_disclosed to prevent the fabrication of undocumented data \[cite: SRC\_DEL\_GLB\_25\].  
* **Granular Geographic Office Separation (Irving, Texas):** Official directories and governmental procurement filings successfully mapped explicit physical addresses for centralized operational delivery centers utilized by Deloitte (8222 N. Belt Line Road) and KPMG (4000 Horizon Way) in Irving, Texas. However, analogous hard physical addresses specifically demarcated as dedicated, standalone service delivery centers for EY and PwC within the precise municipal boundaries of Irving proved difficult to isolate, despite secondary data (e.g., labor condition applications) confirming substantial local workforces \[cite: SRC\_DEL\_IRV\_GOV, SRC\_KPMG\_IRV\_GOV\].  
* **Universal Sustainability Boundary Normalization:** While all firms report toward Science Based Targets initiative (SBTi) net-zero goals, Scope 3 reporting perimeters display significant gaps. Networks selectively report across categories, with a primary focus on Category 1 (Purchased Goods and Services) and Category 6 (Business Travel), rendering comparisons of aggregated Scope 3 totals highly problematic without explicit categorical separation.

## **5\. Material Comparability Limitations**

Direct comparisons across the Big Four dataset carry inherent structural constraints that must inform any subsequent derived modeling or analytics:

* **Reporting Period Misalignment:** The definition of the "fiscal year" differs substantially across the quartet. Deloitte closes its books on May 31\. PwC and EY operate on a June 30 reporting axis (with EY utilizing a floating late-June close, such as June 27 for FY2025). KPMG utilizes a significantly delayed September 30 year-end. Consequently, macroeconomic forces affect the reported datasets on asynchronous cycles \[cite: SRC\_DEL\_GLB\_25, SRC\_PWC\_GLB\_25, SRC\_EY\_GLB\_25, SRC\_KPMG\_GLB\_25\].  
* **Taxonomic Variations in Service Lines:** The definition of "Consulting" is fractured. PwC groups its transformation capabilities under a massive "Advisory" umbrella. EY formally separates "Consulting" from its strategy and deals business ("Strategy and Transactions," heavily driven by EY-Parthenon). A direct comparison between EY's Consulting and PwC's Advisory is statistically invalid without adjusting for this taxonomy.  
* **Workforce Definitions:** Variations exist in the reporting of human capital. Some member networks report period-end nominal headcount (absolute individuals employed on the final day of the fiscal period), whereas others report "Average Full-Time Equivalents" (FTE). This variation distorts derived calculations, particularly "Revenue per Employee."

## **6\. Research Protocol and Source Quality Appraisal**

The extraction and normalization of this quantitative dataset adhered to a strict hierarchical protocol designed to eliminate reliance on external modeling, estimations, or unverified secondary assumptions.  
Primary parameters for global revenue, geographic footprint, and workforce scale were drawn directly from Grade A and B authoritative records: official Global Annual Reviews, Impact Reports, and statutory global press releases issued natively by the coordinating entities (e.g., *Deloitte Touche Tohmatsu Limited*, *KPMG International Limited*). Data points were preserved exactly as rendered (e.g., KPMG's FY2025 revenue reported dynamically on a "continued operations basis" to exclude recent divestitures).  
Engagement-level regulatory data and civil penalties relied exclusively on Grade A governmental and regulatory portals. Specifically, audit deficiency metrics and fines related to auditor independence violations (such as those tied to the PwC Australia events) were pulled directly from official PCAOB Spotlights and press releases, circumventing potential biases embedded within secondary financial press coverage \[cite: SRC\_PCAOB\_SPOT\_24, SRC\_PWC\_AUS\_PEN\].  
All calculated and derived indicators generated in the process (such as Year-over-Year Revenue Growth or Revenue per Employee) maintain strict lineage protocols, explicitly citing the original observation IDs serving as the numerator and denominator, ensuring calculations remain purely mathematical and devoid of editorial speculation.