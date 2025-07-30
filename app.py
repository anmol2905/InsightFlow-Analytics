from cmath import nan
from datetime import date
import streamlit as st
from helper import data, seconddata, match_elements, describe, outliers, drop_items, download_data, filter_data, num_filter_data, rename_columns, clear_image_cache, handling_missing_values, data_wrangling
import numpy as np
import pandas as pd

st.set_page_config(
     page_title="📊 InsightFlow Analytics",
     page_icon="🔍",
     layout="wide",
     initial_sidebar_state="expanded",
     menu_items={
         'Get Help': 'https://github.com/everydaycodings/Data-Analysis-Web-App',
         'Report a bug': "https://github.com/everydaycodings/Data-Analysis-Web-App/issues/new",
         'About': "# 🚀 InsightFlow Analytics \n *Your gateway to powerful data insights!*"
     }
)

# Custom CSS for theme customization
st.markdown("""
<style>
    /* Main app background - Professional beige */
    .stApp {
        background-color: #FAF8F3;
        background-image: 
            linear-gradient(45deg, rgba(139, 69, 19, 0.02) 25%, transparent 25%), 
            linear-gradient(-45deg, rgba(139, 69, 19, 0.02) 25%, transparent 25%), 
            linear-gradient(45deg, transparent 75%, rgba(139, 69, 19, 0.02) 75%), 
            linear-gradient(-45deg, transparent 75%, rgba(139, 69, 19, 0.02) 75%);
        background-size: 60px 60px;
        background-position: 0 0, 0 30px, 30px -30px, -30px 0px;
    }
    
    /* Sidebar - Professional dark theme */
    .stSidebar {
        background: linear-gradient(180deg, #2C3E50 0%, #34495E 100%);
        border-right: 3px solid #BDC3C7;
    }
    
    .stSidebar .stSidebar-content {
        background: transparent;
    }
    
    /* Sidebar text styling - Enhanced visibility */
    .stSidebar h1, .stSidebar h2, .stSidebar h3 {
        color: #FFFFFF !important;
        font-weight: 700;
        text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.5);
    }
    
    .stSidebar .stMarkdown p {
        color: #FFFFFF !important;
        font-weight: 500;
        text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.3);
    }
    
    /* Sidebar labels and text */
    .stSidebar label {
        color: #FFFFFF !important;
        font-weight: 600;
        text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.5);
    }
    
    /* Sidebar file uploader text */
    .stSidebar .stFileUploader label {
        color: #FFFFFF !important;
        font-weight: 600;
    }
    
    /* Sidebar multiselect label */
    .stSidebar .stMultiSelect label {
        color: #FFFFFF !important;
        font-weight: 600;
    }
    
    /* Sidebar selectbox label */  
    .stSidebar .stSelectbox label {
        color: #FFFFFF !important;
        font-weight: 600;
    }
    
    /* Sidebar text input label */
    .stSidebar .stTextInput label {
        color: #FFFFFF !important;
        font-weight: 600;
    }
    
    /* Sidebar help text */
    .stSidebar .help {
        color: #E8E8E8 !important;
    }
    
    /* Sidebar divider */
    .stSidebar hr {
        border-color: #5D6D7E;
        margin: 1rem 0;
    }
    
    /* Professional button styling */
    .stButton > button {
        background: linear-gradient(135deg, #3498DB 0%, #2980B9 100%);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.5rem 1.5rem;
        font-weight: 600;
        letter-spacing: 0.5px;
        box-shadow: 0 2px 8px rgba(52, 152, 219, 0.3);
        transition: all 0.3s ease;
        text-transform: uppercase;
        font-size: 0.85rem;
    }
    
    .stButton > button:hover {
        background: linear-gradient(135deg, #2980B9 0%, #1F4E79 100%);
        box-shadow: 0 4px 12px rgba(52, 152, 219, 0.4);
        transform: translateY(-1px);
    }
    
    /* Data containers - Clean white with subtle shadow */
    .stDataFrame, .element-container .stDataFrame > div {
        background-color: #FFFFFF;
        border-radius: 12px;
        box-shadow: 0 2px 15px rgba(0, 0, 0, 0.08);
        border: 1px solid #E8E8E8;
        padding: 1rem;
    }
    
    /* Info boxes - Professional styling */
    .stAlert {
        border-radius: 10px;
        border-left: 4px solid #3498DB;
        background-color: rgba(255, 255, 255, 0.95);
        backdrop-filter: blur(5px);
    }
    
    /* Select boxes - Corporate styling */
    .stSelectbox > div > div {
        background-color: #FFFFFF;
        border: 2px solid #D5D8DC;
        border-radius: 8px;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
    }
    
    .stSelectbox > div > div:focus-within {
        border-color: #3498DB;
        box-shadow: 0 0 0 3px rgba(52, 152, 219, 0.1);
    }
    
    /* Multiselect - Professional styling */
    .stMultiSelect > div > div {
        background-color: #FFFFFF;
        border: 2px solid #D5D8DC;
        border-radius: 8px;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
    }
    
    .stMultiSelect > div > div:focus-within {
        border-color: #3498DB;
        box-shadow: 0 0 0 3px rgba(52, 152, 219, 0.1);
    }
    
    /* Input fields */
    .stTextInput > div > div > input {
        background-color: #FFFFFF;
        border: 2px solid #D5D8DC;
        border-radius: 8px;
        padding: 0.75rem;
        font-size: 1rem;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #3498DB;
        box-shadow: 0 0 0 3px rgba(52, 152, 219, 0.1);
    }
    
    /* Headers - Professional typography */
    h1, h2, h3 {
        color: #2C3E50 !important;
        font-weight: 700;
        letter-spacing: -0.5px;
    }
    
    h1 {
        border-bottom: 3px solid #3498DB;
        padding-bottom: 0.5rem;
    }
    
    /* Metrics and KPI styling */
    .metric-container {
        background: linear-gradient(135deg, #FFFFFF 0%, #F8F9FA 100%);
        border-radius: 12px;
        padding: 1.5rem;
        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
        border-left: 4px solid #3498DB;
    }
    
    /* File uploader */
    .stFileUploader > div {
        background-color: #FFFFFF;
        border: 2px dashed #BDC3C7;
        border-radius: 12px;
        padding: 2rem;
        text-align: center;
    }
    
    .stFileUploader > div:hover {
        border-color: #3498DB;
        background-color: #F8F9FA;
    }
    
    /* Radio buttons - Corporate style */
    .stRadio > div {
        background-color: rgba(255, 255, 255, 0.8);
        border-radius: 8px;
        padding: 1rem;
        border: 1px solid #E8E8E8;
    }
    
    /* Expander - Professional */
    .streamlit-expanderHeader {
        background-color: #34495E;
        color: white;
        border-radius: 8px;
        font-weight: 600;
    }
    
    .streamlit-expanderContent {
        background-color: #FFFFFF;
        border: 1px solid #E8E8E8;
        border-radius: 0 0 8px 8px;
    }
    
    /* Charts background */
    .js-plotly-plot {
        background-color: #FFFFFF !important;
        border-radius: 12px;
        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
    }
    
    /* Footer styling */
    .stMarkdown p {
        color: #5D6D7E;
    }
    
    /* Custom scrollbar */
    ::-webkit-scrollbar {
        width: 8px;
        height: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: #F1F2F6;
        border-radius: 4px;
    }
    
    ::-webkit-scrollbar-thumb {
        background: #BDC3C7;
        border-radius: 4px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: #95A5A6;
    }
</style>

""", unsafe_allow_html=True)

st.sidebar.title("🔍 InsightFlow Analytics")
st.sidebar.markdown("---")

file_format_type = ["csv", "txt", "xls", "xlsx", "ods", "odt"]
functions = [
    "📋 Overview", 
    "⚠️ Outliers", 
    "🗑️ Drop Columns", 
    "🔻 Drop Categorical Rows", 
    "🔢 Drop Numeric Rows", 
    "✏️ Rename Columns", 
    "📊 Display Plot", 
    "🛠️ Handling Missing Data", 
    "🔧 Data Wrangling"
]
excel_type =["vnd.ms-excel","vnd.openxmlformats-officedocument.spreadsheetml.sheet", "vnd.oasis.opendocument.spreadsheet", "vnd.oasis.opendocument.text"]

uploaded_file = st.sidebar.file_uploader("📂 Upload Your Dataset", type=file_format_type, help="Supported formats: CSV, TXT, XLS, XLSX, ODS, ODT")

if uploaded_file is not None:

    file_type = uploaded_file.type.split("/")[1]
    
    if file_type == "plain":
        seperator = st.sidebar.text_input("🔗 Enter data separator:", max_chars=5, placeholder="e.g., , or ; or |") 
        data = data(uploaded_file, file_type,seperator)

    elif file_type in excel_type:
        data = data(uploaded_file, file_type)

    else:
        data = data(uploaded_file, file_type)
    
    describe, shape, columns, num_category, str_category, null_values, dtypes, unique, str_category, column_with_null_values = describe(data)

    multi_function_selector = st.sidebar.multiselect(
        "🎯 Select Analysis Tools:", 
        functions, 
        default=["📋 Overview"],
        help="Choose one or more analysis tools to explore your data"
    )

    st.markdown("## 📊 Dataset Preview")
    st.dataframe(data, use_container_width=True)

    st.markdown("---")

    if "📋 Overview" in multi_function_selector:
        st.markdown("## 📈 Dataset Analysis Overview")
        
        with st.expander("📋 Statistical Description", expanded=True):
            st.write(describe)

        st.markdown("### 📊 Key Dataset Metrics")

        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown("#### 💾 Basic Information")
            st.info(f"**📄 Dataset Name:** {uploaded_file.name}")
            
            file_size = round((uploaded_file.size*0.000977)*0.000977,2)
            st.info(f"**💽 Size:** {file_size} MB")
            
            st.info(f"**📐 Shape:** {shape}")
            
        with col2:
            st.markdown("#### 📝 Dataset Columns")
            st.success(f"**Total Columns:** {columns}")
        
        with col3:
            st.markdown("#### 🔢 Numeric Columns")
            st.dataframe(num_category, use_container_width=True)
        
        with col4:
            st.markdown("#### 🔤 Text Columns")
            st.dataframe(str_category, use_container_width=True)

        col5, col6, col7, col8= st.columns(4)

        with col5:
            st.markdown("#### ❌ Missing Values")
            st.dataframe(null_values, use_container_width=True)

        with col6:
            st.markdown("#### 🏷️ Data Types")
            st.dataframe(dtypes, use_container_width=True)
        
        with col7:
            st.markdown("#### 🎯 Unique Values Count")
            st.write(unique)

# ==================================================================================================
    if "⚠️ Outliers" in multi_function_selector:
        st.markdown("## ⚠️ Outlier Detection & Analysis")
        
        outliers_selection = st.multiselect(
            "🎯 Select numeric columns to analyze outliers:", 
            num_category,
            help="Choose columns to generate box plots for outlier detection"
        )
        
        if outliers_selection:
            outliers_plots = outliers(data, outliers_selection)
            
            st.markdown("### 📊 Outlier Visualization")
            for i, plot in enumerate(outliers_plots):
                st.markdown(f"#### 📈 Outliers in: **{outliers_selection[i]}**")
                st.image(plot)
        else:
            st.info("👆 Please select at least one numeric column to analyze outliers")

# ===================================================================================================

    if "🗑️ Drop Columns" in multi_function_selector:
        st.markdown("## 🗑️ Column Removal Tool")
        
        multiselected_drop = st.multiselect(
            "🎯 Select columns to remove:", 
            data.columns,
            help="Choose one or multiple columns you want to drop from the dataset"
        )
        
        if multiselected_drop:
            droped = drop_items(data, multiselected_drop)
            
            st.markdown("### ✅ Updated Dataset")
            st.success(f"Successfully removed {len(multiselected_drop)} column(s)")
            st.dataframe(droped, use_container_width=True)
            
            drop_export = download_data(droped, label="✨ Download Cleaned Dataset")
        else:
            st.info("👆 Select columns you want to remove from your dataset")

# =====================================================================================================================================
    if "🔻 Drop Categorical Rows" in multi_function_selector:
        st.markdown("## 🔻 Categorical Data Filtering")

        filter_column_selection = st.selectbox(
            "📋 Select column to filter:", 
            options=data.columns,
            help="Choose the column containing categorical values you want to filter"
        )
        
        filtered_value_selection = st.multiselect(
            f"🎯 Select values to REMOVE from '{filter_column_selection}' column:", 
            data[filter_column_selection].unique(),
            help="Select one or more values that you want to exclude from your dataset"
        )
        
        if filtered_value_selection:
            filtered_data = filter_data(data, filter_column_selection, filtered_value_selection)
            
            st.markdown("### ✅ Filtered Dataset")
            st.success(f"Removed rows containing: {', '.join(map(str, filtered_value_selection))}")
            st.dataframe(filtered_data, use_container_width=True)
            
            filtered_export = download_data(filtered_data, label="🔽 Download Filtered Data")
        else:
            st.info("👆 Select values you want to remove from the dataset")

# =============================================================================================================================

    if "🔢 Drop Numeric Rows" in multi_function_selector:
        st.markdown("## 🔢 Numeric Data Range Filtering")

        option = st.radio(
            "🎯 Choose filtering method:",
            ('🗑️ Delete data inside the range', '✂️ Delete data outside the range'),
            help="Choose whether to remove data within or outside the selected range"
        )

        num_filter_column_selection = st.selectbox(
            "📊 Select numeric column:", 
            options=num_category,
            help="Choose the numeric column you want to filter"
        )
        
        if num_filter_column_selection:
            selection_range = data[num_filter_column_selection].unique()

            for i in range(0, len(selection_range)) :
                selection_range[i] = selection_range[i]
            selection_range.sort()

            selection_range = [x for x in selection_range if np.isnan(x) == False]

            start_value, end_value = st.select_slider(
                '🎚️ Select value range:',
                options=selection_range,
                value=(min(selection_range), max(selection_range)),
                help="Drag the slider to select the range of values"
            )
            
            if option == "🗑️ Delete data inside the range":
                st.warning(f'⚠️ Removing all values between **{int(start_value)}** and **{int(end_value)}**')
                num_filtered_data = num_filter_data(data, start_value, end_value, num_filter_column_selection, param="Delete data inside the range")
            else:
                st.info(f'✂️ Keeping only values between **{int(start_value)}** and **{int(end_value)}**')
                num_filtered_data = num_filter_data(data, start_value, end_value, num_filter_column_selection, param="Delete data outside the range")

            st.markdown("### ✅ Filtered Dataset")
            st.dataframe(num_filtered_data, use_container_width=True)
            num_filtered_export = download_data(num_filtered_data, label="🔢 Download Numeric Filtered Data")

# =======================================================================================================================================

    if "✏️ Rename Columns" in multi_function_selector:
        st.markdown("## ✏️ Column Renaming Tool")

        if 'rename_dict' not in st.session_state:
            st.session_state.rename_dict = {}

        rename_column_selector = st.selectbox(
            "📝 Select column to rename:", 
            options=data.columns,
            help="Choose the column you want to rename"
        )
        
        rename_text_data = st.text_input(
            f"✨ Enter new name for '{rename_column_selector}':",
            max_chars=50,
            placeholder="Enter new column name..."
        )

        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("📝 Draft Changes", help="Save your rename changes to draft before applying"):
                if rename_text_data:
                    st.session_state.rename_dict[rename_column_selector] = rename_text_data
                    st.success(f"✅ Drafted: '{rename_column_selector}' → '{rename_text_data}'")
                else:
                    st.error("❌ Please enter a new column name")

        with col2:
            if st.button("🚀 Apply Changes", help="Apply all drafted column renames"):
                if st.session_state.rename_dict:
                    rename_column = rename_columns(data, st.session_state.rename_dict)
                    
                    st.markdown("### ✅ Updated Dataset with New Column Names")
                    st.dataframe(rename_column, use_container_width=True)
                    
                    export_rename_column = download_data(rename_column, label="✏️ Download Renamed Dataset")
                    st.session_state.rename_dict = {}
                    st.success("🎉 Column renaming completed successfully!")
                else:
                    st.error("❌ No changes drafted. Please draft changes first.")

        if st.session_state.rename_dict:
            st.markdown("### 📋 Drafted Changes:")
            st.code(st.session_state.rename_dict)

# ===================================================================================================================
 
    if "📊 Display Plot" in multi_function_selector:
        st.markdown("## 📊 Data Visualization")

        multi_bar_plotting = st.multiselect(
            "🎯 Select categorical columns to visualize:", 
            str_category,
            help="Choose columns to generate bar charts showing value distributions"
        )
        
        if multi_bar_plotting:
            for i, column in enumerate(multi_bar_plotting):
                st.markdown(f"### 📊 Distribution of **{column}**")
                
                try:
                    # Get value counts and create a proper DataFrame
                    value_counts = data[column].value_counts().reset_index()
                    value_counts.columns = [column, 'Count']
                    
                    # Sort by count for better visualization
                    value_counts = value_counts.sort_values('Count', ascending=False)
                    
                    # Limit to top 20 values for better readability
                    if len(value_counts) > 20:
                        value_counts = value_counts.head(20)
                        st.info(f"📋 Showing top 20 most frequent values out of {len(data[column].unique())} unique values")
                    
                    # Create the bar chart with explicit y parameter
                    st.bar_chart(
                        value_counts.set_index(column),
                        y='Count',
                        use_container_width=True,
                        height=400
                    )
                    
                    # Add some insights
                    total_unique = len(data[column].unique())
                    most_common = data[column].value_counts().index[0]
                    most_common_count = data[column].value_counts().values[0]
                    
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("🎯 Unique Values", total_unique)
                    with col2:
                        st.metric("🏆 Most Common", most_common)
                    with col3:
                        st.metric("📊 Frequency", most_common_count)
                        
                except Exception as e:
                    st.error(f"❌ Error creating chart for column '{column}': {str(e)}")
                    st.info("💡 Try using a different column or check your data for mixed types")
                    
                    # Show alternative - simple value counts table
                    st.markdown(f"#### 📋 Value Distribution Table for **{column}**")
                    value_counts_table = data[column].value_counts().head(10)
                    st.dataframe(value_counts_table, use_container_width=True)
                
                st.markdown("---")  # Add separator between charts
        else:
            st.info("👆 Select categorical columns to generate visualizations")


# ====================================================================================================================    

    if "🛠️ Handling Missing Data" in multi_function_selector:
        st.markdown("## 🛠️ Missing Data Management")
        
        handling_missing_value_option = st.radio(
            "🎯 Choose your approach:", 
            ("🗑️ Drop Null Values", "🔧 Fill Missing Values"),
            help="Select how you want to handle missing data in your dataset"
        )

        if handling_missing_value_option == "🗑️ Drop Null Values":
            st.markdown("### 🗑️ Remove Missing Data")

            drop_null_values_option = st.radio(
                "📋 Select removal strategy:", 
                ("🚫 Drop all rows with any null values", "⚠️ Drop only rows with all null values"),
                help="Choose how aggressive you want to be with removing missing data"
            )
            
            droped_null_value = handling_missing_values(data, drop_null_values_option)
            
            st.markdown("### ✅ Cleaned Dataset")
            rows_removed = len(data) - len(droped_null_value)
            st.success(f"🎉 Removed **{rows_removed}** rows with missing data")
            st.dataframe(droped_null_value, use_container_width=True)
            
            export_cleaned_data = download_data(droped_null_value, label="🧹 Download Cleaned Dataset")
        
        elif handling_missing_value_option == "🔧 Fill Missing Values":
            st.markdown("### 🔧 Fill Missing Values")
            
            if 'missing_dict' not in st.session_state:
                st.session_state.missing_dict = {}
            
            if column_with_null_values:
                fillna_column_selector = st.selectbox(
                    "📋 Select column with missing values:", 
                    options=column_with_null_values,
                    help="Choose the column where you want to fill missing values"
                )
                
                fillna_text_data = st.text_input(
                    f"✨ Enter replacement value for '{fillna_column_selector}' missing data:",
                    max_chars=50,
                    placeholder="e.g., 0, 'Unknown', mean, median..."
                )

                col1, col2 = st.columns(2)
                
                with col1:
                    if st.button("📝 Draft Fill Value", help="Save your fill value to draft before applying"):     
                        if fillna_text_data:
                            if fillna_column_selector in num_category:
                                try:
                                    st.session_state.missing_dict[fillna_column_selector] = float(fillna_text_data)
                                    st.success(f"✅ Drafted numeric fill: {fillna_text_data}")
                                except:
                                    try:
                                        st.session_state.missing_dict[fillna_column_selector] = int(fillna_text_data)
                                        st.success(f"✅ Drafted integer fill: {fillna_text_data}")
                                    except:
                                        st.error("❌ Please enter a valid number for numeric column")
                            else:
                                st.session_state.missing_dict[fillna_column_selector] = fillna_text_data
                                st.success(f"✅ Drafted text fill: '{fillna_text_data}'")
                        else:
                            st.error("❌ Please enter a replacement value")

                with col2:
                    if st.button("🚀 Apply Fill Values", help="Apply all drafted fill values to missing data"):
                        if st.session_state.missing_dict:
                            fillna_column = handling_missing_values(data, handling_missing_value_option, st.session_state.missing_dict)
                            
                            st.markdown("### ✅ Dataset with Filled Values")
                            st.dataframe(fillna_column, use_container_width=True)
                            
                            export_filled_data = download_data(fillna_column, label="🔧 Download Filled Dataset")
                            st.session_state.missing_dict = {}
                            st.success("🎉 Missing values filled successfully!")
                        else:
                            st.error("❌ No fill values drafted. Please draft changes first.")

                if st.session_state.missing_dict:
                    st.markdown("### 📋 Drafted Fill Values:")
                    st.code(st.session_state.missing_dict)
            else:
                st.info("🎉 Great! No missing values found in your dataset!")

# ==========================================================================================================================================

    if "🔧 Data Wrangling" in multi_function_selector:
        st.markdown("## 🔧 Advanced Data Wrangling")
        
        data_wrangling_option = st.radio(
            "🎯 Choose data combination method:", 
            ("🔗 Merging On Common Column", "📚 Concatenating Datasets"),
            help="Select how you want to combine your datasets"
        )

        if data_wrangling_option == "🔗 Merging On Common Column":
            st.markdown("### 🔗 Dataset Merging")
            
            data_wrangling_merging_uploaded_file = st.file_uploader(
                "📂 Upload second dataset to merge:", 
                type=uploaded_file.name.split(".")[1],
                help="Upload a file with the same format to merge with your current dataset"
            )

            if data_wrangling_merging_uploaded_file is not None:
                second_data = seconddata(data_wrangling_merging_uploaded_file, file_type=data_wrangling_merging_uploaded_file.type.split("/")[1])
                same_columns = match_elements(data, second_data)
                
                if same_columns:
                    merge_key_selector = st.selectbox(
                        "🔑 Select merge key (common column):", 
                        options=same_columns,
                        help="Choose the common column to merge both datasets"
                    )
                    
                    merge_data = data_wrangling(data, second_data, merge_key_selector, "Merging On Index")
                    
                    st.markdown("### ✅ Merged Dataset")
                    st.success(f"🎉 Successfully merged datasets on column: **{merge_key_selector}**")
                    st.dataframe(merge_data, use_container_width=True)
                    
                    download_data(merge_data, label="🔗 Download Merged Dataset")
                else:
                    st.error("❌ No common columns found between the datasets for merging!")

        if data_wrangling_option == "📚 Concatenating Datasets":
            st.markdown("### 📚 Dataset Concatenation")

            data_wrangling_concatenating_uploaded_file = st.file_uploader(
                "📂 Upload second dataset to concatenate:", 
                type=uploaded_file.name.split(".")[1],
                help="Upload a file to stack vertically with your current dataset"
            )

            if data_wrangling_concatenating_uploaded_file is not None:
                second_data = seconddata(data_wrangling_concatenating_uploaded_file, file_type=data_wrangling_concatenating_uploaded_file.type.split("/")[1])
                concatenating_data = data_wrangling(data, second_data, None, "Concatenating On Axis")
                
                st.markdown("### ✅ Concatenated Dataset")
                st.success("🎉 Successfully concatenated datasets vertically!")
                st.dataframe(concatenating_data, use_container_width=True)
                
                download_data(concatenating_data, label="📚 Download Concatenated Dataset")
        
# ==========================================================================================================================================
    
    st.sidebar.markdown("---")
    st.sidebar.warning("🧹 **Important:** Clear cache after analysis to remove temporary files and protect your data privacy.")
    
    if st.sidebar.button("🗑️ Clear Cache & Clean Up", help="Remove all temporary files and cached data"):
        clear_image_cache()
        st.sidebar.success("✅ Cache cleared successfully!")

else:
    # Welcome screen when no file is uploaded
    st.markdown("# 🔍 Welcome to InsightFlow Analytics!")
    st.markdown("### 🚀 Your Gateway to Powerful Data Analysis")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("""
        #### 🎯 What can you do with InsightFlow?
        
        - **📊 Data Overview:** Get comprehensive dataset statistics and insights
        - **⚠️ Outlier Detection:** Identify and visualize data anomalies  
        - **🛠️ Data Cleaning:** Remove unwanted columns and rows
        - **✏️ Column Management:** Rename columns for better clarity
        - **📈 Visualizations:** Generate insightful charts and plots
        - **🔧 Missing Data Handling:** Clean and fill missing values
        - **🔗 Data Wrangling:** Merge and concatenate multiple datasets
        
        #### 🎨 Supported File Formats:
        📄 CSV • 📝 TXT • 📊 XLS/XLSX • 📋 ODS • 📑 ODT
        """)
    
    with col2:
        st.markdown("#### 🎁 Try with Sample Data")
        with open('samples/sample.zip', 'rb') as f:
            st.download_button(
                label="📦 Download Sample Dataset",
                data=f,
                file_name='sample_data.zip',
                help="Download sample data to explore InsightFlow features",
                use_container_width=True
            )
    
    st.markdown("---")
    st.info("👆 **Get Started:** Upload your dataset using the file uploader in the sidebar!")
