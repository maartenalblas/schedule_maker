import web
import hill_climber
import csv

urls = ('/', 'Index',
        '/schedule', 'Schedule')

render = web.template.render('templates/')

class Index:
    def GET(self):
        return render.index()
    def POST(self):
        data = web.input(courses={}, students={}, rooms={})
        table_data, capacity_minus, student_minnus, frequency_minus = hill_climber.main(data)
        header = ['Course', 'Type', 'Day', 'Block', 'Room']
        return render.schedule(header, table_data, capacity_minus, student_minnus, frequency_minus)

if __name__ == "__main__":
   app = web.application(urls, globals())
   app.run()
