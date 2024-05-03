import os
import webbrowser


class InterfaceTools:

    # Ask user to select city
    def get_city(self):

        user_input = input('>>> Do you want to look for new jobs in Köln or in Bonn? Type "1" for Köln. Type "2" for Bonn.\n')

        if user_input == '1' or user_input == '2':
            city_ = 'Köln' if user_input == '1' else 'Bonn'
            os.system('clear')
            return city_
        else:
            os.system('clear') 
            print('''>>> Wrong input!\n''')
            return self.get_city()
        
    # Ask user whether to open serach results in browser
    def open_results(self, city):
        user_input = input('>>> Do you want to open the search results in your web browser? Type "1" for yes. Type "2" to finish.\n')
        if user_input == "1":
            webbrowser.open('file://' + os.getcwd() + f'/results/jobs_{city}.html')
            exit()
        elif user_input == "2":
            exit()
        else:
            os.system('clear') 
            print('''>>> Wrong input!\n''')
            self.open_results(city)

    # Transform databank entries to html