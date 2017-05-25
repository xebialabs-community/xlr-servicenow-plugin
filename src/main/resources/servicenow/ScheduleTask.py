#
# Copyright 2017 XEBIALABS
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#


from java.util import Date
from java.text import ParseException
from java.text import SimpleDateFormat
from sets import Set
from java.util import TimeZone

formatter = SimpleDateFormat( snFormat )
xlrFormat = SimpleDateFormat( xlFormat )
formatter.setTimeZone(TimeZone.getTimeZone(snTimeZone))

startDate = snData[startField]
print "------"
try:
    print "Schedule Task=> date = %s" % (startDate)
    date = formatter.parse(startDate)
    print "Schedule Task=> date = %s" % (date)
    release = getCurrentRelease()
    releaseID = release.id
    phaseTitle=targetPhase
    taskTitle=targetTask
    print "Schedule Task=> Phase / Task = %s / %s" % ( phaseTitle, taskTitle )
    phase = phaseApi.searchPhasesByTitle( phaseTitle, releaseID )
    print "Schedule Task=> phase = %s" % ( phase )
    phaseID = phase[0].id
    task = taskApi.searchTasksByTitle( taskTitle, phaseTitle, releaseID)
    print "Schedule Task=> task = %s" % ( task )
    taskID = task[0].id
    myTask = taskApi.getTask( taskID )
    myTask.waitForScheduledStartDate = True
    myTask.scheduledStartDate = xlrFormat.format(date)
    print "Schedule Task=> Task = %s" % ( myTask )
    print "Schedule Task=> Task.scheduledStartDate = %s" % ( myTask.scheduledStartDate )
    taskApi.updateTask( myTask )

except ParseException :
    print "exception
# End try
print "------"
