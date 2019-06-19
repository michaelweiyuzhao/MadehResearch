import csv
import pyodbc

def main():
    # Settings
    settings = {}
    
    # Import settings from config file
    with open('config.txt') as configfile:
        rdr = csv.reader(configfile, delimiter=':')
        for row in rdr:
            try:
                if row[0].strip() == 'Database driver':
                    settings['Database driver'] = row[1].strip()
                elif row[0].strip() == 'Server name':
                    settings['Server name'] = row[1].strip()
                elif row[0].strip() == 'Database name':
                    settings['Database name'] = row[1].strip()
                elif row[0].strip() == 'Custom setup':
                    settings['Custom setup'] = row[1].strip()
            except:
                pass
                
    
    # Ask user whether or not they want to run custom setup
    if settings['Custom setup'] == 'true' or settings['Custom setup'] == 'True':
        
        start_option = input('Would you like to run custom setup?\
        \nDefault values ('+settings['Database driver']+','+settings['Server name']+\
        ','+settings['Database name']+') (y/n): ')
        print('')
    
        if start_option == 'y' or start_option == 'yes' or start_option == 'Yes':
            print('Please be advised these custom settings are temporary. To permanently change settings\
                please change \'config.txt\' in the \'program\' folder.')
            settings['Database driver'] = input('Specify custom driver (default is '+settings['Database driver']+').')
            settings['Server name'] = input('Specify custom server (default is '+settings['Server name']+').')
            settings['Database name'] = input('Specify custom database (default is '+settings['Database name']+').')
        elif start_option != 'n' and start_option != 'no' and start_option != 'No':
            print('User input was not y or n, program will continue without setup.')
    
        print('')        
            
    elif settings['Custom setup'] == 'false' or settings['Custom setup'] == 'False':
        
        print('Custom setup skipped, program will continue with default values from \'config.txt\' located in the \'program\' folder')
        print('('+settings['Database driver']+','+settings['Server name']+\
        ','+settings['Database name']+')')
        print('To enable custom setup, please change the value of \'Custom setup\' setting in \'config.txt\' to \'True\'')
        print('')
        
    else:
        
        print('The value for the \'Custom setup\' setting in \'config.txt\' was neither \'True\' nor \'False\'')
        print('Program will continue with default values from \'config.txt\' located in the \'program\' folder')
        print('')
        
    
    # Attempt to connect to database
    print("Attempting to connect to database...")
    
    try:
        conn = pyodbc.connect(
            r'Driver='+settings['Database driver']+';'
            r'Server='+settings['Server name']+';'
            r'Database='+settings['Database name']+';'
            r'Trusted_Connection=yes;'
            )
    except Exception as e:
        print('Error connecting to database, check your settings and try again')
        print(str(e))
        print('Exiting program...')
        return
        
    print("Successfully connected to database")
    print('')
    
    cursor = conn.cursor()
    
    
    # Open settings files and parse queries/error checks
    print('Parsing queries from queries.txt and keyword_replacements.txt...')
    
    queries = []
    replacements = {}
    
    # Parse query file
    with open('queries.txt') as queryfile:
        rdr = csv.reader(queryfile, delimiter='|')
        for row in rdr:
            queries.append(row)
    
    if not queries:
        print('queries.txt is empty, please configure queries.txt')
        print('Exiting program...')
        return
    
    # Parser replacement file
    with open('keyword_replacements.txt') as replacefile:
        rdr = csv.reader(replacefile, delimiter=',')
        for row in rdr:
            try:
                if row[0] not in replacements:
                    replacements[row[0]] = []
                replacements[row[0]].append(row[1])
            except:
                pass
    
    iterations = 0
    if not replacements:
        print('keyword_replacements.txt is empty. Program will not replace any values in queries.txt')
        print('If this is unintended, please configure keyword_replacements.txt')
    else:
        iterations = len(next(iter(replacements.values())))
        for entry in replacements.values():
            if len(entry) != iterations:
                print('Missmatch of number of different keywords in keyword_replacements.txt.')
                print('Please make sure there are equal numbers of every keyword in keyword_replacements.txt')
                print('Exiting program...')
                return
    
    print('')
    
    
#==============================================================================
#     # Ask user for year range
#     years_input_flag = False
#     while years_input_flag == False:
#         years_raw = input('Please specify a range of years (YYYY YYYY): ')
#         try:
#             years = years_raw.split(' ')
#             years = list(map(int,years))
#             years_input_flag = True
#         except:
#             print('Invalid range format, try again.')
#             years_input_flag = False
#     
#     # Ask user for years offset
#     offset_input_flag = False
#     while offset_input_flag == False:
#         year_offset_raw = input('Please specify years to offset (#): ')
#         try:
#             year_offset = int(year_offset_raw)
#             offset_input_flag = True
#         except:
#             print('Invalid offset format, try again.')
#             offset_input_flag = False
#==============================================================================
    
    
    # Iterate through years and execute queries
    print('Running queries...')
    print('')
    for i in range(0,iterations-1):
        for query_dict in queries:
            for query in query_dict:
                            
                # Change keywords for this iteration
                for key, value in replacements.items():
                    query = query.replace(key, value[i])
                    
                # Execute query
                try:
                    cursor.execute('SET NOCOUNT ON')
                    cursor.execute(query)
                except BaseException as e:
                    print('Failed to execute query on iteration '+str(i)+' due to the following error:')
                    print(str(e))
                    print('')
                        
    
    # Exit
    print('')
    print('Program finished.')
    exit_command = input('Commit work? Database will not be updated unless you enter \'y\'. (y/n): ')
    
    if exit_command == 'y':
        print('Saving work and exiting...')
        conn.commit()
    else:
        print('Discarding work and exiting...')
        
    conn.close()
    
    return
    
if __name__ == '__main__':
    main()