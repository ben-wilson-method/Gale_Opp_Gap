import streamlit as st

#Import the standard modules
import pandas as pd
pd.set_option('display.max_columns', None)
import numpy as np
import matplotlib.pyplot as plt
import pickle


#Import the data
uploaded_file = st.file_uploader("Upload the Opp Gap Survey file")

if uploaded_file is not None:
    # Unpack the data
    with uploaded_file as file:
        Save_list = pickle.load(file)
    df,Questions,Question_numbers,group_dic,Question_dic,Question_label_replacement,Single_column_dic,reorder_list = Save_list
    
    Question_num = st.sidebar.selectbox("Which question to analyse",Question_numbers)
    
    #Create the sidebar
    st.sidebar.write('Which groups would you like to compare?')
    group_list = []
    for key in group_dic.keys():
        if st.sidebar.checkbox(key,key=key):
            group_list.append(key)
            
            
    
    st.subheader(Question_num)
    if Single_column_dic[Question_num] == 'Multi':
        st.write(Question_label_replacement[Question_num].replace(' - Selected Choice -',''))
    if Single_column_dic[Question_num] == 'Single':
        st.write(Questions[Question_dic[Question_num]][0])
        
    if group_list == []:
        st.write('#')
        st.write(f':red[Waiting for you to select which groups to compare]')
    else:
        if Single_column_dic[Question_num] == 'Multi':
            Question_df = df[Question_dic[Question_num]]
            for col in Question_df.columns:
                Question_df[col] = [1 if type(i) == str else 0 for i in Question_df[col].tolist()]
        if Single_column_dic[Question_num] == 'Single':
            if Question_num in reorder_list.keys():
                cols = reorder_list[Question_num]
            else:
                cols = df[Question_dic[Question_num][0]].value_counts().keys()
            Question_df = pd.DataFrame(columns=cols)
            for j,el in enumerate(df[Question_dic[Question_num][0]].tolist()):
                temp_dic = {cols[i]:0 for i in range(len(cols))}
                if type(el) == str:
                    temp_dic[el] = 1
                Question_df = pd.concat([Question_df,pd.DataFrame([temp_dic])])
            Question_df.columns = cols
        
        #Create the plot
        fig,ax = plt.subplots()

        num_groups = len(group_list)

        label_dic = {key:i for i,key in enumerate(Question_df.mean().keys())}
        width = 1/(num_groups+1)
        multiplier = 0
        for group in group_list:
            working_dic = Question_df.iloc[group_dic[group]].mean()
            x_axis = np.array([label_dic[key] for key in working_dic.keys()])
            offset = width * multiplier
            if sum(working_dic.values) == 0:
                ax.bar(x_axis+offset,0,width = width,label=group)
            else:
                ax.bar(x_axis+offset,100*working_dic.values/sum(working_dic.values),width = width,label=group)
            multiplier += 1

        relabel_dic = Questions[Question_dic[Question_num]].str.replace(Question_label_replacement[Question_num],'')

        if Single_column_dic[Question_num] == 'Multi':
            ax.set_xticks(np.array(list(label_dic.values())) + 1/2 - width, relabel_dic[label_dic.keys()],rotation=90)
            #ax.set_xticks(np.array(list(label_dic.values())), relabel_dic[label_dic.keys()],rotation=90)
        if Single_column_dic[Question_num] == 'Single':
            ax.set_xticks(np.array(list(label_dic.values())) + 1/2 - width, cols,rotation=90)
            #ax.set_xticks(np.array(list(label_dic.values())), cols,rotation=90)
        ax.legend()
        ax.set_ylabel('Percentage of cohort to select')
        st.pyplot(fig)
        
        
else:
    st.write("##")
    st.subheader('Waiting for the Data')
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
