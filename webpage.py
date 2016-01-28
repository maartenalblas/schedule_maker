import web
import hill_climber
import csv
# import HTML

urls = ('/', 'Index',
        '/schedule', 'Schedule')

render = web.template.render('templates/')

class Index:
    def GET(self):
        return render.index()
    def POST(self):
        data = web.input(courses={}, students={}, rooms={})
        table_data = hill_climber.main(data)
        header = ['Course', 'Type', 'Day', 'Block', 'Room', '#Students', "Capacity"]
        return render.schedule(header, table_data)

if __name__ == "__main__":
   app = web.application(urls, globals())
   app.run()
