import pandas as pd

ava_data = pd.read_csv('./datasets/ava_dataset/ava_train/ava_train_v2.2.csv', header=None)
#ava_data.info()


prova = ava_data.groupby([0, 1, 7])[7].count()
#prova = ava_data.groupby([0, 1]).ngroups
#df['distinct_count'] = df.groupby(['param'])['group'].transform('nunique')

print(prova)

# Convert the result into a DataFrame
result_df = prova.reset_index(name='Count')

# Rename the columns for clarity
result_df.rename(columns={0: 'A', 1: 'B', 2:'C', 3: 'Count'}, inplace=True)

# Print the result DataFrame
print(result_df)

prova2 = result_df.groupby(['A', 'B']).count()==1
#print(prova2)

result_df2 = prova2

# Rename the columns for clarity
result_df2.rename(columns={0: 'A', 1: 'B', 2:'C', 3: 'Count'}, inplace=True)
#print(result_df2)

true_rows = result_df2[result_df2[7] & result_df2['Count']]
print(true_rows)

print(true_rows.keys)