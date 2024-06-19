import pandas as pd


def calculate_demographic_data(print_data=True):
    # Read data from file
    df = pd.read_csv('adult.data.csv')

    # How many of each race are represented in this dataset? This should be a Pandas series with race names as the index labels.
    race_count = pd.Series(df.groupby(['race']).size(), index=df.race.unique())

    # What is the average age of men?
    average_age_men = df[df['sex'] == 'Male']['age'].mean().round(1)

    # What is the percentage of people who have a Bachelor's degree?
    percentage_bachelors = ((df[df['education'] == 'Bachelors']['education'].count() / df['education'].count()) * 100).round(1)

    # What percentage of people with advanced education (`Bachelors`, `Masters`, or `Doctorate`) make more than 50K?
    # What percentage of people without advanced education make more than 50K?

    # with and without `Bachelors`, `Masters`, or `Doctorate`
    higher_education = df[((df.education == 'Bachelors') | (df.education == 'Masters') | (df.education == 'Doctorate'))]['salary']
    lower_education = df[((df.education != 'Bachelors') & (df.education != 'Masters') & (df.education != 'Doctorate'))]['salary']

    # percentage with salary >50K
    higher_education_rich = ((higher_education[higher_education == '>50K'].count() / higher_education.count()) * 100).round(1)
    lower_education_rich = ((lower_education[lower_education == '>50K'].count() / lower_education.count()) * 100).round(1)

    # What is the minimum number of hours a person works per week (hours-per-week feature)?
    min_work_hours = pd.Series(df['hours-per-week']).min()

    # What percentage of the people who work the minimum number of hours per week have a salary of >50K?
    num_min_workers = df[df['hours-per-week'] == min_work_hours]['salary']

    rich_percentage = ((num_min_workers[num_min_workers == '>50K'].count() / num_min_workers.count()) * 100).round(1)

    # What country has the highest percentage of people that earn >50K?
    totalCounts = df['native-country'].value_counts().reset_index()
    totalCounts.columns = ['native-country','total_count']
    filtered_df = df[df['salary'] == '>50K']
    gt50k_counts = filtered_df['native-country'].value_counts().reset_index()
    gt50k_counts.columns = ['native-country', 'gt50k_count']
    merged_counts = pd.merge(totalCounts, gt50k_counts, on='native-country', how='left')
    merged_counts['gtk50_count'] = merged_counts['gt50k_count'].fillna(0)
    merged_counts['percentage'] = (merged_counts['gt50k_count'] / merged_counts['total_count']) * 100
    max_percentage_country = merged_counts.loc[merged_counts['percentage'].idxmax()]

    highest_earning_country = max_percentage_country['native-country']
    highest_earning_country_percentage = max_percentage_country['percentage'].round(1)

    # Identify the most popular occupation for those who earn >50K in India.
    filteredDF = df[(df['salary'] == '>50K') & (df['native-country'] == 'India')]
    occupation_counts = filteredDF['occupation'].value_counts().reset_index()
    occupation_counts.columns = ['occupation','count']
    most_popular_occupation = occupation_counts.loc[occupation_counts['count'].idxmax()]

    top_IN_occupation = most_popular_occupation['occupation']

    # DO NOT MODIFY BELOW THIS LINE

    if print_data:
        print("Number of each race:\n", race_count) 
        print("Average age of men:", average_age_men)
        print(f"Percentage with Bachelors degrees: {percentage_bachelors}%")
        print(f"Percentage with higher education that earn >50K: {higher_education_rich}%")
        print(f"Percentage without higher education that earn >50K: {lower_education_rich}%")
        print(f"Min work time: {min_work_hours} hours/week")
        print(f"Percentage of rich among those who work fewest hours: {rich_percentage}%")
        print("Country with highest percentage of rich:", highest_earning_country)
        print(f"Highest percentage of rich people in country: {highest_earning_country_percentage}%")
        print("Top occupations in India:", top_IN_occupation)

    return {
        'race_count': race_count,
        'average_age_men': average_age_men,
        'percentage_bachelors': percentage_bachelors,
        'higher_education_rich': higher_education_rich,
        'lower_education_rich': lower_education_rich,
        'min_work_hours': min_work_hours,
        'rich_percentage': rich_percentage,
        'highest_earning_country': highest_earning_country,
        'highest_earning_country_percentage':
        highest_earning_country_percentage,
        'top_IN_occupation': top_IN_occupation
    }
