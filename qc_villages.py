import pandas as pd

filename = "2024-05-02_Village_Regions.xlsx"
gov_filename = "GOV_Village_Regions.xlsx"
df_fs = pd.read_excel(filename, sheet_name="REGION_Village")
df_gov = pd.read_excel(gov_filename, sheet_name="data.gov.in")


df_fs["full_district_name"] = df_fs["r_001_state_name"].str.cat(
    df_fs[["r_002_dis_name"]], sep=":"
)


df_fs["full_taluka_name"] = df_fs["r_001_state_name"].str.cat(
    df_fs[
        [
            "r_002_dis_name",
            "r_003_tal_name",
        ]
    ],
    sep=":",
)

df_fs["full_village_name"] = df_fs["r_001_state_name"].str.cat(
    df_fs[
        [
            "r_002_dis_name",
            "r_003_tal_name",
            "r_004_vill_name",
        ]
    ],
    sep=":",
)

# df_fs["full_village_name"] = df_fs["r_61_state_id"].str.cat(
#     df_fs[
#         [
#             "r_62_dis_id",
#             "r_63_tal_id",
#             "r_64_vill_id",
#         ]
#     ],
#     sep=":",
# )

df_fs["full_district_name"] = df_fs["full_district_name"].str.lower()
df_fs["full_taluka_name"] = df_fs["full_taluka_name"].str.lower()
df_fs["full_village_name"] = df_fs["full_village_name"].str.lower()
df_fs["full_village_name_original"] = df_fs["full_village_name"]

fs_districts = df_fs["full_district_name"].unique().tolist()
fs_talukas = df_fs["full_taluka_name"].unique().tolist()
fs_villages = df_fs["full_village_name"].unique().tolist()


df_gov["full_district_name"] = df_gov["STATE NAME"].str.cat(
    df_gov[["DISTRICT NAME"]], sep=":"
)
df_gov["full_taluka_name"] = df_gov["STATE NAME"].str.cat(
    df_gov[["DISTRICT NAME", "SUB-DISTRICT NAME"]], sep=":"
)
df_gov["full_village_name"] = df_gov["STATE NAME"].str.cat(
    df_gov[["DISTRICT NAME", "SUB-DISTRICT NAME", "Area Name"]], sep=":"
)

df_gov["full_district_name"] = df_gov["full_district_name"].str.lower()
df_gov["full_taluka_name"] = df_gov["full_taluka_name"].str.lower()
df_gov["full_village_name"] = df_gov["full_village_name"].str.lower()
df_fs['r_001_state_name'] = df_fs['r_001_state_name'].str.lower()

dg_districts = df_gov["full_district_name"].unique().tolist()
dg_talukas = df_gov["full_taluka_name"].unique().tolist()
dg_villages = df_gov["full_village_name"].unique().tolist()

district_names = list(set(dg_districts).difference(set(fs_districts)))
taluka_names = list(set(dg_talukas).difference(set(fs_talukas)))
village_names = list(set(dg_villages).difference(set(fs_villages)))

district_names = sorted(district_names)
taluka_names = sorted(taluka_names)
village_names = sorted(village_names)

# dictionary of lists
# fs_district_dict = {"fs_district": fs_districts}
# fs_taluka_dict = {"fs_talukas": fs_talukas}
dg_district_dict = {"dg_district": dg_districts}
dg_taluka_dict = {"dg_talukas": dg_talukas}

# fs_district_df = pd.DataFrame(fs_district_dict)
# fs_taluka_df = pd.DataFrame(fs_taluka_dict)
dg_district_df = pd.DataFrame(dg_district_dict)
dg_taluka_df = pd.DataFrame(dg_taluka_dict)

#splits up the whole name for diff district table
diff_district_df = pd.DataFrame(district_names, columns=['Total'])
split_values = diff_district_df['Total'].str.split(pat=":", expand=True)
diff_district_df['State'] = split_values[0]
diff_district_df['District'] = split_values[1]

#splits up the whole name for diff talukas table
diff_taluka_df = pd.DataFrame(taluka_names, columns=['Total'])
split_values = diff_taluka_df['Total'].str.split(pat=":", expand=True)
diff_taluka_df['State'] = split_values[0]
diff_taluka_df['District'] = split_values[1]
diff_taluka_df['Taluka'] = split_values[2]

#splits up the whole name for diff villages table
diff_village_df = pd.DataFrame(village_names, columns=['Total'])
split_values = diff_village_df['Total'].str.split(pat=":", expand=True)
diff_village_df['State'] = split_values[0]
diff_village_df['District'] = split_values[1]
diff_village_df['Taluka'] = split_values[2]
diff_village_df['Village'] = split_values[3]

#splits up the whole name for farmsetu district table
fs_district_df = pd.DataFrame(fs_districts, columns=['Total1'])
split_values = fs_district_df['Total1'].str.split(pat=":", expand=True)
fs_district_df['State Name'] = split_values[0]
fs_district_df['District Name'] = split_values[1]
fs_district_df = fs_district_df.drop(['Total1'],axis=1)
# fs_district_df['State ID'] = df_fs["r_61_state_id"]
# fs_district_df["District ID"] = df_fs["r_62_dis_id"]

#splits up the whole name for farmsetu taluka table
fs_taluka_df = pd.DataFrame(fs_talukas, columns=['Total1'])
split_values = fs_taluka_df['Total1'].str.split(pat=":", expand=True)
fs_taluka_df['State Name'] = split_values[0]
fs_taluka_df['District Name'] = split_values[1]
fs_taluka_df['Taluka Name'] = split_values[2]
fs_taluka_df = fs_taluka_df.drop(['Total1'],axis=1)
# fs_taluka_df["State ID"] = df_fs["r_61_state_id"]
# fs_taluka_df["District ID"] = df_fs["r_62_dis_id"]
# fs_taluka_df["Taluka ID"] = df_fs["r_63_tal_id"]

#splits up the whole name for farmsetu villages table(not unique but converted to lowercase so as to maintain the id correspondence
split_values = df_fs["full_village_name_original"].str.split(pat=":", expand=True)
fs_village_df = pd.DataFrame()
fs_village_df['State Name'] = split_values[0]
fs_village_df['District Name'] = split_values[1]
fs_village_df['Taluka Name'] = split_values[2]
fs_village_df['Village Name'] = split_values[3]
#fs_taluka_df = fs_taluka_df.drop(['full_village_name_original'],axis=1)
fs_village_df["State ID"] = df_fs["r_61_state_id"]
fs_village_df["District ID"] = df_fs["r_62_dis_id"]
fs_village_df["Taluka ID"] = df_fs["r_63_tal_id"]
# fs_taluka_df["Village ID"] = df_fs["r_64_vill_id"]

#do we really need to compare fs district and talukas coz they are the same talukas is just a bigger set and wroks for all soo?

#merges dfs

#works for uptil district level
diff_district_df.info()
fs_district_df.info()
# df_fs['r_001_state_name'] = df_fs['r_001_state_name'].lower()
diff_district_df = pd.merge(diff_district_df,  fs_village_df, left_on="State",right_on='State Name', how="left")
diff_district_df = diff_district_df.drop_duplicates(subset=['District'],keep='first')
diff_district_df = diff_district_df.drop(['Total', 'State Name', 'District Name','Taluka Name','Village Name', 'District ID', 'Taluka ID'], axis=1)

# works for uptil taluka level
diff_taluka_df = pd.merge(diff_taluka_df, fs_village_df, left_on="District",right_on='District Name', how="left")
diff_taluka_df = diff_taluka_df.drop_duplicates(subset=['Taluka'],keep='first')
diff_taluka_df = diff_taluka_df.drop(['Total', 'State Name', 'District Name','Taluka Name','Village Name', 'Taluka ID'], axis=1)

# works for uptil village level
diff_village_df = pd.merge(diff_village_df, fs_village_df, left_on="Taluka",right_on='Taluka Name', how="left")
diff_village_df = diff_village_df.drop_duplicates(subset=['Village'],keep='first')
diff_village_df = diff_village_df.drop(['Total', 'State Name', 'District Name','Taluka Name','Village Name'], axis=1)

# fs_district_df= fs_district_df.assign(State=lambda x: fs_district_df['Total'].str.split(pat=":")[0])
# diff_district_df = pd.DataFrame(diff_district_dict)
# diff_taluka_df = pd.DataFrame(diff_taluka_dict)
# diff_village_df = pd.DataFrame(diff_village_dict)
# fs_district_df = pd.DataFrame({"fs_state": fs_district_df.str.split(pat=":")[0], "fs_district": fs_district_df.str.split(pat=":")[1]})
# fs_taluka_df = pd.DataFrame({"fs_state": fs_taluka_df.str.split(pat=":")[0], "fs_district": fs_taluka_df.str.split(pat=":")[1],"fs_talukas": fs_taluka_df.str.split(pat=":")[2]})
# dg_district_df = pd.DataFrame({"dg_state": dg_district_df.str.split(pat=":")[0], "dg_district": dg_district_df.str.split(pat=":")[1]})
# dg_taluka_df = pd.DataFrame({"dg_state": dg_taluka_df.str.split(pat=":")[0], "dg_district": dg_taluka_df.str.split(pat=":")[1],"dg_talukas": dg_taluka_df.str.split(pat=":")[2]})
# diff_district_df = pd.DataFrame({"diff_state": diff_district_df.str.split(pat=":")[0], "diff_district": diff_district_df.str.split(pat=":")[1]})
# diff_taluka_df = pd.DataFrame({"diff_state": diff_taluka_df.str.split(pat=":")[0], "diff_district": diff_taluka_df.str.split(pat=":")[1],"diff_talukas": diff_taluka_df.str.split(pat=":")[2]})
# diff_village_df = pd.DataFrame({"diff_state": diff_village_df.str.split(pat=":")[0], "diff_district": diff_village_df.str.split(pat=":")[1],"diff_talukas": diff_village_df.str.split(pat=":")[2],"diff_villages": diff_village_df.str.split(pat=":")[3]})

with pd.ExcelWriter(f"QC_{filename}", engine="xlsxwriter") as writer:
    df_fs.to_excel(writer, sheet_name="FS", index=False)
    df_gov.to_excel(writer, sheet_name="GOV", index=False)
    fs_district_df.to_excel(writer, sheet_name="FS-DIS", index=False)
    fs_taluka_df.to_excel(writer, sheet_name="FS-TAL", index=False)
    fs_village_df.to_excel(writer, sheet_name="FS-VIL", index=False)
    dg_district_df.to_excel(writer, sheet_name="GOV-DIS", index=False)
    dg_taluka_df.to_excel(writer, sheet_name="GOV-TAL", index=False)
    diff_district_df.to_excel(writer, sheet_name="Diff-GOV-DIS", index=False)
    # merged_df.to_excel(writer, sheet_name="Merged_-DIS", index=False)
    diff_taluka_df.to_excel(writer, sheet_name="Diff-GOV-TAL", index=False)
    diff_village_df.to_excel(writer, sheet_name="Diff-GOV-VIL", index=False)

print("Completed")
