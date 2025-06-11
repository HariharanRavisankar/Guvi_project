import streamlit as st
import pandas as pd
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

conn =psycopg2.connect(database ="police_log", host = "localhost",user = "postgres",password="2244",port=5432)
conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
cursor =conn.cursor()

def fetch(query):
    cursor.execute(query)
    result = cursor.fetchall()
    Data = pd.DataFrame(result)
    return Data


st.markdown(
    "<h1 style='text-align: center;'>Police Checkpost Log</h1>",
    unsafe_allow_html=True
)
#1.What are the top 10 vehicle_Number involved in drug-related stops?
st.header("1.Drug_related top 10 data")
query=("""select vehicle_number
            from "LOG"
            Where drugs_related_stop is True
            LIMIT 10""")
Drug_related=fetch(query)
colnames = [desc[0] for desc in cursor.description]
df = pd.DataFrame(Drug_related,columns=colnames)
st.dataframe(Drug_related)


#2. Which vehicles were most frequently searched?
st.header("2.Frequently searched vehicle")
query=("""select vehicle_number, count(*) AS frequency
        from "LOG"
        Where search_conducted is True
        GROUP BY vehicle_number
        order by frequency DESC
        LIMIT 5""")
Frequently_searched_vehicle=fetch(query)
st.dataframe(Frequently_searched_vehicle,use_container_width=True)

#4. Which driver age group had the highest arrest rate?
st.header("3.Frequently arrested Age Group")
query=("""select driver_age, count(*) AS frequency
        from "LOG"
        Where is_arrested is True
        GROUP BY driver_age
        order by frequency DESC
        LIMIT 5""")
Frequently_arrested_Age_Group=fetch(query)
st.dataframe(Frequently_arrested_Age_Group,use_container_width=True)

#5. What is the gender distribution of drivers stopped in each country?
st.header("4.gender distribution in each country")
query=("""select country_name, driver_gender, count(*)AS total_stop
        from "LOG"
        GROUP BY country_name,driver_gender
        order by country_name,total_stop DESC;""")
gender_distribution=fetch(query)
st.dataframe(gender_distribution)


#Which race and gender combination has the highest search rate?
st.header("5.Highest race and gender combination of searches")
query=("""select driver_race, driver_gender, count(*)AS total_stops,SUM(CASE when search_conducted Then 1 else 0 End) as searches
        from "LOG"
        GROUP BY driver_race,driver_gender
        order by SUM(case when search_conducted then 1 else 0 end)::float/count(*) DESC
        limit 1""")
gender_and_race=fetch(query)
st.dataframe(gender_and_race)


#7. What time of day sees the most traffic stops?
st.header("6.Average stop time")
query=("""SELECT violation, ROUND(AVG(case when stop_duration= '0-15 Min' Then 7.5 when stop_duration= '16-30 Min' then 23 when stop_duration= '30+ Min' then 35 ELSE Null end),2) AS avg_stop_duration
        FROM "LOG"
        GROUP BY violation
        ORDER BY avg_stop_duration DESC;""")
gender_and_race=fetch(query)
st.dataframe(gender_and_race)

#8. What is the average stop duration for different violations?
st.header("7.Most traffic stops")
query=("""SELECT violation, ROUND(AVG(case when stop_duration= '0-15 Min' Then 7.5 when stop_duration= '16-30 Min' then 23 when stop_duration= '30+ Min' then 35 ELSE Null end),2) AS avg_stop_duration
        FROM "LOG"
        GROUP BY violation
        ORDER BY avg_stop_duration DESC;""")
traffic_stops=fetch(query)
st.dataframe(traffic_stops)


#9. Are stops during the night more likely to lead to arrests?
st.header("8.Are stops during the night more likely to lead to arrests?")
query=("""SELECT
  CASE WHEN EXTRACT(HOUR FROM "DateTime"::timestamp) BETWEEN 6 AND 17 THEN 'Day' ELSE 'Night'
  END AS time_of_day,COUNT(*) AS total_stops,SUM(CASE WHEN is_arrested THEN 1 ELSE 0 END) AS arrests,
  ROUND(100.0 * SUM(CASE WHEN is_arrested THEN 1 ELSE 0 END)::numeric / COUNT(*), 2) AS arrest_rate_percent
FROM "LOG"
WHERE "DateTime" IS NOT NULL AND is_arrested IS NOT NULL
GROUP BY time_of_day
ORDER BY arrest_rate_percent DESC;""")
day_and_night=fetch(query)
st.dataframe(day_and_night)



#10.Which violations are most associated with searches or arrests?
st.header("9.Violations associated with search and arrest")
query=("""SELECT
  violation,
  COUNT(*) AS total_stops,
  SUM(CASE WHEN search_conducted THEN 1 ELSE 0 END) AS searches,
  ROUND(
    100.0 * SUM(CASE WHEN search_conducted THEN 1 ELSE 0 END)::numeric / COUNT(*),
    2
  ) AS search_rate_percent
FROM
  "LOG"
WHERE
  violation IS NOT NULL
GROUP BY
  violation
ORDER BY
  search_rate_percent DESC;""")
search_and_arrest=fetch(query)
st.dataframe(search_and_arrest)


#11.Which violations are most common among younger drivers (<25)?
st.header("10.Common violation among young driver(<25)")
query=("""SELECT
  violation,
  COUNT(*) AS total_stops
FROM
  "LOG"
WHERE
  driver_age < 25
  AND violation IS NOT NULL
GROUP BY
  violation
ORDER BY
  total_stops DESC;""")
violation_young=fetch(query)
st.dataframe(violation_young)


#12.Is there a violation that rarely results in search or arrest?
st.header("11.voilation rarely result in serch and arrest")
query=("""SELECT
  violation,
  COUNT(*) AS total_stops,
  SUM(CASE WHEN search_conducted THEN 1 ELSE 0 END) AS total_searches,
  ROUND(
    100.0 * SUM(CASE WHEN search_conducted THEN 1 ELSE 0 END)::numeric / COUNT(*), 2
  ) AS search_rate_percent
FROM
  "LOG"
WHERE
  violation IS NOT NULL
GROUP BY
  violation
HAVING COUNT(*) > 10  -- optional: filter out rare violations
ORDER BY
  search_rate_percent ASC
LIMIT 5;""")
violation_rarely_serch=fetch(query)
st.dataframe(violation_rarely_serch)



#13.Which countries report the highest rate of drug-related stops?
st.header("12.country-wise Drug related stops")
query=("""SELECT
  country_name,
  COUNT(*) AS total_stops,
  SUM(CASE WHEN drugs_related_stop THEN 1 ELSE 0 END) AS drug_stops,
  ROUND(
    100.0 * SUM(CASE WHEN drugs_related_stop THEN 1 ELSE 0 END)::numeric / COUNT(*),
    2
  ) AS drug_stop_rate_percent
FROM
  "LOG"
WHERE
  country_name IS NOT NULL
GROUP BY
  country_name
ORDER BY
  drug_stop_rate_percent DESC;""")
drug_stops_country=fetch(query)
st.dataframe(drug_stops_country)


#14.What is the arrest rate by country and violation?
st.header("13.arrest rate by country and violation")
query=("""SELECT
  country_name,
  violation,
  COUNT(*) AS total_stops,
  SUM(CASE WHEN is_arrested THEN 1 ELSE 0 END) AS total_arrests,
  ROUND(
    100.0 * SUM(CASE WHEN is_arrested THEN 1 ELSE 0 END)::numeric / COUNT(*),
    2
  ) AS arrest_rate_percent
FROM
  "LOG"
WHERE
  country_name IS NOT NULL AND violation IS NOT NULL
GROUP BY
  country_name, violation
ORDER BY
  arrest_rate_percent DESC;""")
arrest_rate_percentage=fetch(query)
st.dataframe(arrest_rate_percentage)


#15.Which country has the most stops with search conducted?
st.header("14.most stoped and searched country")
query=("""SELECT
  country_name,
  COUNT(*) AS total_searches
FROM
  "LOG"
WHERE
  search_conducted = TRUE
  AND country_name IS NOT NULL
GROUP BY
  country_name
ORDER BY
  total_searches DESC
LIMIT 1;""")
total_search_arrest=fetch(query)
st.dataframe(total_search_arrest)



#1.Yearly Breakdown of Stops and Arrests by Country (Using Subquery and Window Functions)
st.header("15.yearly data for country wise")
query=("""SELECT
  country_name,
  year,
  total_stops,
  total_arrests,
  ROUND(100.0 * total_arrests::numeric / total_stops, 2) AS arrest_rate_percent,
  SUM(total_stops) OVER (PARTITION BY country_name ORDER BY year) AS cumulative_stops,
  SUM(total_arrests) OVER (PARTITION BY country_name ORDER BY year) AS cumulative_arrests
FROM (
  SELECT
    country_name,
    EXTRACT(YEAR FROM "DateTime"::timestamp) AS year,
    COUNT(*) AS total_stops,
    SUM(CASE WHEN is_arrested THEN 1 ELSE 0 END) AS total_arrests
  FROM
    "LOG"
  WHERE
    "DateTime" IS NOT NULL
    AND country_name IS NOT NULL
  GROUP BY
    country_name, year
) AS yearly_data
ORDER BY
  country_name, year;""")
yearly_data=fetch(query)
st.dataframe(yearly_data)


#2.Driver Violation Trends Based on Age and Race (Join with Subquery)
st.header("16.violation based on Age and Race")
query=("""WITH age_grouped AS (
    SELECT
        driver_race,
        violation,
        CASE
            WHEN driver_age < 20 THEN '<20'
            WHEN driver_age BETWEEN 20 AND 29 THEN '20-29'
            WHEN driver_age BETWEEN 30 AND 39 THEN '30-39'
            WHEN driver_age BETWEEN 40 AND 49 THEN '40-49'
            WHEN driver_age BETWEEN 50 AND 59 THEN '50-59'
            WHEN driver_age BETWEEN 60 AND 69 THEN '60-69'
            WHEN driver_age BETWEEN 70 AND 79 THEN '70-79'
            ELSE '80+'
        END AS age_group
    FROM "LOG"
)
SELECT
    age_group,
    driver_race,
    violation,
    COUNT(*) AS count
FROM age_grouped
GROUP BY age_group, driver_race, violation
ORDER BY count DESC;
""")
Age_and_race=fetch(query)
st.dataframe(Age_and_race)


#3.Time Period Analysis of Stops (Joining with Date Functions) , Number of Stops by Year,Month, Hour of the Day
st.header("17.Time period analysis")
query=("""SELECT
    EXTRACT(YEAR FROM "DateTime"::timestamp) AS stop_year,
    EXTRACT(MONTH FROM "DateTime"::timestamp) AS stop_month,
    EXTRACT(HOUR FROM "DateTime"::timestamp) AS stop_hour,
    COUNT(*) AS number_of_stops
FROM "LOG"
GROUP BY stop_year, stop_month, stop_hour
ORDER BY stop_year, stop_month, stop_hour;
""")
Time_period=fetch(query)
st.dataframe(Time_period)



#4.Violations with High Search and Arrest Rates (Window Function)
st.header("18.voilation with highest search and Arrest")
query=("""
    SELECT violation,
    COUNT(*) AS total_stops,
    SUM(CASE WHEN search_conducted THEN 1 ELSE 0 END) AS total_searches,
    SUM(CASE WHEN is_arrested THEN 1 ELSE 0 END) AS total_arrests,
    ROUND(100.0 * SUM(CASE WHEN search_conducted THEN 1 ELSE 0 END) / COUNT(*), 2) AS search_rate_percent,
    ROUND(100.0 * SUM(CASE WHEN is_arrested THEN 1 ELSE 0 END) / COUNT(*), 2) AS arrest_rate_percent,
    RANK() OVER (ORDER BY SUM(CASE WHEN search_conducted THEN 1 ELSE 0 END)::float / COUNT(*) DESC) AS search_rate_rank,
    RANK() OVER (ORDER BY SUM(CASE WHEN is_arrested THEN 1 ELSE 0 END)::float / COUNT(*) DESC) AS arrest_rate_rank
FROM "LOG"
GROUP BY violation
ORDER BY search_rate_percent DESC;
""")
search_and_arrest1=fetch(query)
st.dataframe(Time_period)


#5.Driver Demographics by Country (Age, Gender, and Race)
st.header("19.Driver's Demographics")
query=("""
    SELECT
    country_name,
    ROUND(AVG(driver_age), 1) AS avg_age,
    
    COUNT(*) FILTER (WHERE driver_gender = 'M') AS male_count,
    COUNT(*) FILTER (WHERE driver_gender = 'F') AS female_count,
    ROUND(100.0 * COUNT(*) FILTER (WHERE driver_gender = 'M') / COUNT(*), 2) AS male_percent,
    ROUND(100.0 * COUNT(*) FILTER (WHERE driver_gender = 'F') / COUNT(*), 2) AS female_percent,
    
    COUNT(*) FILTER (WHERE driver_race = 'White') AS white_count,
    COUNT(*) FILTER (WHERE driver_race = 'Black') AS black_count,
    COUNT(*) FILTER (WHERE driver_race = 'Asian') AS asian_count,
    COUNT(*) FILTER (WHERE driver_race = 'Other') AS other_count
    
FROM "LOG"
GROUP BY country_name
ORDER BY country_name;
""")
Driver_demographics=fetch(query)
st.dataframe(Driver_demographics)



#6.Top 5 Violations with Highest Arrest Rates
st.header("20.Top 5 highest Arrest rates")
query=("""
    SELECT
    violation,
    COUNT(*) AS total_stops,
    SUM(CASE WHEN is_arrested THEN 1 ELSE 0 END) AS total_arrests,
    ROUND(100.0 * SUM(CASE WHEN is_arrested THEN 1 ELSE 0 END) / COUNT(*), 2) AS arrest_rate_percent
FROM "LOG"
GROUP BY violation
HAVING COUNT(*) > 0  -- Avoid division by zero
ORDER BY arrest_rate_percent DESC
LIMIT 5;
""")
arrest_rate=fetch(query)
st.dataframe(arrest_rate)




st.title("Add a Traffic Stop Record")

with st.form("stop_form"):
    date_time = st.text_input("Date & Time (YYYY-MM-DD HH:MM:SS)")
    driver_age = st.number_input("Driver Age", min_value=0)
    driver_race = st.selectbox("Driver Race", ["White", "Black", "Asian", "Other"])
    driver_gender = st.radio("Driver Gender", ["M", "F"])
    country = st.text_input("Country")
    violation = st.text_input("Violation")
    search_conducted = st.checkbox("Was Search Conducted?")
    is_arrested = st.checkbox("Was Arrest Made?")

    submitted = st.form_submit_button("Submit")

    if submitted:
        try:
            # Insert query
            cursor.execute("""
                INSERT INTO "LOG" (
                    "DateTime", driver_age, driver_race, driver_gender, country_name,
                    violation, search_conducted, is_arrested
                )
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """, (date_time, driver_age, driver_race, driver_gender, country,
                  violation, search_conducted, is_arrested))

            conn.commit()
            st.success("Record added successfully!")

        except Exception as e:
            conn.rollback()
            st.error(f"Error inserting record: {e}")