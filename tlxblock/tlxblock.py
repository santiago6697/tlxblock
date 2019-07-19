"""TO-DO: Write a description of what this XBlock is."""

import os                                   # This module is required to access ENV vars.
import json                                 # This module is required to parse text into JSON.
import requests                             # This module is used to perform HTTP requests.
import pkg_resources
from datetime import datetime

from xblock.core import XBlock
from xblock.fields import Integer, Scope
from xblock.fragment import Fragment

# OPEN_EDX_COURSES_API_TOKEN = os.environ['OPEN_EDX_COURSES_API_TOKEN']
# OPEN_EDX_COURSES_API_USERNAME = os.environ['OPEN_EDX_COURSES_API_USERNAME']
# OPEN_EDX_URI = os.environ['OPEN_EDX_URI']
OPEN_EDX_COURSES_API_TOKEN = "6ff56cc112717df4f22d58b1058e60d375979cc6"
OPEN_EDX_COURSES_API_USERNAME = "root"
OPEN_EDX_URI = "http://192.168.33.10/"

class TrafficLightXBlock(XBlock):
    """
    TO-DO: document what your XBlock does.
    """

    # Fields are defined on the class.  You can access them in your code as
    # self.<fieldname>.

    # TO-DO: delete count, and define your own fields.
    count = Integer(
        default=10, scope=Scope.user_state,
        help="A simple counter, to show something happening",
    )

    def resource_string(self, path):
        """Handy helper for getting resources from our kit."""
        data = pkg_resources.resource_string(__name__, path)
        return data.decode("utf8")

    # TO-DO: change this view to display your data your own way.
    def student_view(self, context=None):
        """
        The primary view of the TrafficLightXBlock, shown to students
        when viewing courses.
        """
        html = self.resource_string("static/html/tlxblock.html")
        frag = Fragment(html.format(self=self))
        frag.add_css(self.resource_string("static/css/tlxblock.css"))
        frag.add_javascript(self.resource_string("static/js/src/tlxblock.js"))
        frag.initialize_js('TrafficLightXBlock')
        return frag

    # TO-DO: change this handler to perform your own actions.  You may need more
    # than one handler, or you may not need any handlers at all.
    @XBlock.json_handler
    def traffic_light (self, data, suffix=''):
        res = {}
        try:
            req = api_request(self)
            blocks = json.loads(req.content)['blocks']
            due_date = blocks[str(self.parent)]['due']
            # due_date = blocks["block-v1:edX+DemoX+Demo_Course+type@vertical+block@934cc32c177d41b580c8413e561346b3"]['due']
            due_date = datetime.strptime(due_date, '%Y-%m-%dT%H:%M:%SZ')
            date_now = datetime.now()
            timestamp_delta = (due_date - date_now).total_seconds()
            res = {
                "delta": timestamp_delta,
                "due_date": str(due_date)
            }
        except:
            res = {
                "result": "No content"
            }

        return res
    
    @XBlock.json_handler
    def increment_count(self, data, suffix=''):
        """
        An example handler, which increments the data.
        """
        # Just to show data coming in...
        assert data['hello'] == 'world'

        self.count += 1
        return {"count": self.count}

    # TO-DO: change this to create the scenarios you'd like to see in the
    # workbench while developing your XBlock.
    @staticmethod
    def workbench_scenarios():
        """A canned scenario for display in the workbench."""
        return [
            ("TrafficLightXBlock",
             """<tlxblock/>
             """),
            ("Multiple TrafficLightXBlock",
             """<vertical_demo>
                <tlxblock/>
                <tlxblock/>
                <tlxblock/>
                </vertical_demo>
             """),
        ]

def api_request (self):
    course_id = "course-v1:"+str(self.scope_ids.usage_id.course_key)
    # course_id = "course-v1:edX+DemoX+Demo_Course"
    api_path = "api/courses/v1/blocks/"
    headers = {
        "Authorization": "Bearer "+OPEN_EDX_COURSES_API_TOKEN
    }
    params = {
        "course_id": course_id, # TODO: Obtain it dinamically.
        "username": OPEN_EDX_COURSES_API_USERNAME,
        "requested_fields": "due",
        "depth": "all"
    }
    return requests.get(url = OPEN_EDX_URI+api_path, params = params, headers = headers)
    