/*
 * 
 * This script will add two columns to two different tables.
 * If the tables already have the columns, you will receive an error message, which you can SKIP over.
 * (One error message for each column it tries to add.)
 * 
 * First run the script in Rollback by doing the following:
 * 	1. Highlight the BEGIN TRANSACTION row at the top and run it using the play button.
 * 	2. Highlight the rest of the script and run it using the play scroll button.
 * 		If you see any errors (column already exists) you can skip them.
 * 	3. Analyze the results by checking for 0 and 1 (0 columns found and then 1 of the NEW column found), as well as the Row Counts for each table.
 * 		Row counts SHOULD NOT change, but better just to verify that.
 * 
 * (You can also run BEGIN TRAN using play, highlight the middle, run using scroll play, check results, then highlight either END or ROLLBACK using play to run.
 * 
 * Once you are satisfied with the results, do the same thing to run in COMMIT, except comment out the ROLLBACK and comment IN the END TRANSACTION at the bottom.
 * 
 * This will add a "response_status_ID" column to the quote table (FK to response_status table)
 * And will add a "download_ID" column to the response_status table (Unique ID for each API call group)
 * 
 */

BEGIN TRANSACTION; -- run this first, then run the rest using the scroll play button

SELECT COUNT(*) FROM pragma_table_info('quote') WHERE name='response_status_ID';
SELECT COUNT(*) FROM quote q ;
ALTER TABLE quote ADD response_status_ID INT NULL;
SELECT COUNT(*) FROM pragma_table_info('quote') WHERE name='response_status_ID';
SELECT COUNT(*) FROM quote q ;

SELECT COUNT(*) FROM pragma_table_info('response_status') WHERE name='download_ID';
SELECT COUNT(*) FROM response_status rs ;
ALTER TABLE response_status ADD download_ID INT NULL;
SELECT COUNT(*) FROM pragma_table_info('response_status') WHERE name='download_ID';
SELECT COUNT(*) FROM response_status rs ;

ROLLBACK TRANSACTION;

-- END TRANSACTION;

