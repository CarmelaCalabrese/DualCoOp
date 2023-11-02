import pandas as pd

# ava_data = pd.read_csv('./datasets/ava_dataset/ava_train/ava_train_v2.2.csv', header=None)
# #ava_data.info()

# # Group and count by columns 0, 1, and 7
# result_df = ava_data.groupby([0, 1, 7])[7].count().reset_index(name='Count')

# # Rename the columns for clarity
# result_df.rename(columns={0: 'url_id', 1: 'Second', 7: 'C'}, inplace=True)

# # Group by 'url_id' and 'Second' and check if Count is equal to 1
# result_df2 = result_df.groupby(['url_id', 'Second'])['Count'].count().reset_index(name='Count')
# result_df2 = result_df2[result_df2['Count'] == 1]

# # Remove the 'Count' column and add a new column 'NewColumn'
# result_df2 = result_df2.drop(columns=['Count'])

# # Print the result DataFrame
# print(result_df2.iloc[0])

# print(result_df2.iloc[1])

# # # Merge ava_data and result_df2 on columns A and B
# # merged_data = pd.merge(ava_data, result_df2, left_on=[0, 1], right_on=['url_id', 'Second'], how='inner')

# # # Extract the values from the 6th column of ava_data
# # values_in_6th_column = merged_data[6]

# # # Print the extracted values
# # print(values_in_6th_column)

# # Create a new column in result_df2 with values from ava_data
# #result_df2['NewColumn'] = result_df2.apply(lambda row: ava_data[(ava_data[0] == row['url_id']) & (ava_data[1] == row['Second'])][6].values[0], axis=1)

# ava_data.set_index([0, 1], inplace=True)
# print('Done first step')
# result_df2['NewColumn'] = result_df2.apply(lambda row: ava_data.loc[(row['url_id'], row['Second']), 6], axis=1)


# # Print the updated result_df2
# print(result_df2)

import pandas as pd

# Read the CSV file
ava_data = pd.read_csv('./datasets/ava_dataset/ava_train/ava_train_v2.2.csv', header=None)

#end 51669 98710 155139 249339 311959 378586 473814 565748 654954 714605 793385 862662

# Slice the first rows of ava_data
extreme1 = 793386
extreme2 = 862662
print(ava_data.iloc[extreme1])
print(ava_data.iloc[extreme2])
ava_data = ava_data.iloc[extreme1:extreme2]

# Group and count by columns 0, 1, and 7
result_df = ava_data.groupby([0, 1, 7])[7].count().reset_index(name='Count')

# Rename the columns for clarity
result_df.rename(columns={0: 'url_id', 1: 'Second', 7: 'C'}, inplace=True)

# Group by 'url_id' and 'Second' and check if Count is equal to 1
result_df2 = result_df.groupby(['url_id', 'Second'])['Count'].count().reset_index(name='Count')
result_df2 = result_df2[result_df2['Count'] == 1]

# Remove the 'Count' column 
result_df2 = result_df2.drop(columns=['Count'])
print(result_df2)

# Create a new 'Actions_id' column in result_df2
result_df2['Actions_id'] = [ava_data[(ava_data[0] == row['url_id']) & (ava_data[1] == row['Second'])][6].values for _, row in result_df2.iterrows()]

# Save the result to a CSV file
result_df2.to_csv('output_values.csv', index=False)