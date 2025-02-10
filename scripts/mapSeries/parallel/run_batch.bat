@echo off
setlocal enabledelayedexpansion

:: Set the drive letter where the network path is mapped
set SCRIPT_DIR=E:\mheaton\GitHub\GRID3_mapProduction\mapSeries\parallel\run_batch.bat

:: Navigate to the script directory
pushd %SCRIPT_DIR%

:: Run the Python script to count the number of filtered pages
for /f "delims=" %%i in ('c:/Users/mheaton/AppData/Local/ESRI/conda/envs/arcgispro-py3-mjh/python.exe mapSeries\parallel\count_filtered_pages.py') do set TOTAL_PAGES=%%i

if not defined TOTAL_PAGES (
    echo Failed to count the number of pages.
    popd
    exit /b 1
)

echo Total pages to process: %TOTAL_PAGES%

:: Define the number of instances
set NUM_INSTANCES=4
set /A PAGES_PER_INSTANCE=TOTAL_PAGES / NUM_INSTANCES
set /A REMAINDER=TOTAL_PAGES %% NUM_INSTANCES

:: Calculate the start and end pages for each instance
set START_PAGE=1

for /L %%i in (1, 1, %NUM_INSTANCES%) do (
    set /A END_PAGE=START_PAGE + PAGES_PER_INSTANCE - 1
    if %%i==%NUM_INSTANCES% set /A END_PAGE=END_PAGE + REMAINDER
    echo Running instance %%i: pages !START_PAGE! to !END_PAGE!
    start "" c:/Users/mheaton/AppData/Local/ESRI/conda/envs/arcgispro-py3-mjh/python.exe exportMapSeries.py !START_PAGE! !END_PAGE!
    set /A START_PAGE=END_PAGE + 1
)

popd
endlocal
