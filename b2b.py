
import streamlit as st
import pandas as pd
import io

st.set_page_config(layout="wide")
st.title('Excel File Upload and Display')

# Create sidebar
with st.sidebar:
    st.header('Upload Data')
    uploaded_file = st.file_uploader("Choose an Excel file", type=['xlsx', 'xls'])

if uploaded_file is not None:
    try:
        df = pd.read_excel(uploaded_file)
        st.sidebar.success('File successfully uploaded!')
        
        # Simulator options in sidebar
        st.sidebar.header('Simulator Options')
        cols = df.columns.tolist()
        index = st.sidebar.multiselect('Select Row(s) (Index)', cols)
        columns = st.sidebar.multiselect('Select Column(s)', cols)
        values = st.sidebar.multiselect('Select Value(s)', cols)
        
        agg_functions = ['mean', 'sum', 'count', 'min', 'max']
        aggfunc = st.sidebar.selectbox('Select Aggregation Function', agg_functions)
        
        if st.sidebar.button('Run Simulator'):
            try:
                result_table = pd.pivot_table(df, values=values if values else None, 
                                           index=index if index else None, 
                                           columns=columns if columns else None, 
                                           aggfunc=aggfunc)
                
                # Display results in main area
                st.header('Simulation Results')
                st.write(result_table)
                
                # Download button for simulation results
                csv_result = result_table.to_csv()
                st.download_button(
                    label="Download results as CSV",
                    data=csv_result,
                    file_name='simulation_results.csv',
                    mime='text/csv',
                )
            except Exception as e:
                st.warning('Please select at least one field for values')
    except Exception as e:
        st.sidebar.error(f'Error: {str(e)}')
