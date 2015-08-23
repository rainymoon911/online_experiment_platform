__author__ = 'zhangyanni'
"""TO-DO: Write a description of what this XBlock is."""

import pkg_resources

from xblock.core import XBlock
from xblock.fields import Scope, Integer, String
from xblock.fragment import Fragment

from lib_util import Util

import pymongo
import os

class JennystartXBlock(XBlock):
    """
    TO-DO: document what your XBlock does.
    """

    # Fields are defined on the class.  You can access them in your code as
    # self.<fieldname>.

    # TO-DO: delete count, and define your own fields.
    codeData = String(default="", scope=Scope.user_state, help="codeData")
    file_path=String(default="", scope=Scope.user_state, help="file_path")
    logger = Util .uc_logger()


    # TO-DO: change this view to display your data your own way.
    def student_view(self, context=None):
        """
        The primary view of the JennystartXBlock, shown to students
        when viewing courses.
        """

        student_id=self.runtime.anonymous_student_id
        base_path="/edx/var/edxapp/staticfiles/ucore/"
	real_user = self.runtime.get_real_user(student_id)
	username = real_user.username
        
        conn = pymongo.Connection('localhost', 27017)
        db = conn.test
        codeview = db.codeview
        result = codeview.find_one({"username":username})
        conn.disconnect()
        
	self.logger.info(username + " start edit")
        if result:
            relative_path = result["view_file"]
            self.file_path = base_path + student_id + relative_path
	    self.logger.info("file " + relative_path)
	    output=open(self.file_path)
            self.codeData =output.read()
            output.close()
        else:
            relative_path = "please enter file path"
	    self.file_path = relative_path       
        
        context_dict={"file":relative_path,"codeData":self.codeData}

        fragment = Fragment()
        fragment.add_content(Util.render_template("static/html/jennystart.html",context_dict) )
        fragment.add_css(Util.load_resource("static/css/jennystart.css"))
        fragment.add_css(Util.load_resource("static/css/codemirror.css"))
        fragment.add_css(Util.load_resource("static/css/fullscreen.css"))
      
        fragment.add_javascript(Util.load_resource("static/js/src/jennystart.js"))
        fragment.add_javascript(Util.load_resource("static/js/src/codemirror.js"))
        fragment.add_javascript(Util.load_resource("static/js/src/active-line.js"))
        fragment.add_javascript(Util.load_resource("static/js/src/clike.js"))
        fragment.add_javascript(Util.load_resource("static/js/src/matchbrackets.js"))
        fragment.add_javascript(Util.load_resource("static/js/src/fullscreen.js"))
        fragment.initialize_js('JennystartXBlock')
        return fragment

    # TO-DO: change this handler to perform your own actions.  You may need more
    # than one handler, or you may not need any handlers at all.
    @XBlock.json_handler
    def open_file(self, data, suffix=''):
        """
        An  handler, which read the data.
        """
        
        base_path="/edx/var/edxapp/staticfiles/ucore/"
        relative_path=data['relative_path']
        student_id=self.runtime.anonymous_student_id
        self.file_path=base_path+student_id+relative_path
        output=open(self.file_path)
        self.codeData =output.read()
        output.close()
	return {"codeData":self.codeData}


    @XBlock.json_handler
    def save_file(self, data, suffix=''):
        """
        save_file handler, which save the changed data on codemirror.
        """
        # save the changed datd to file...
        self.logger.info("save_file_invoke")
        self.codeData=data['codeData']
        output=open(self.file_path,"wb")
        output.write(self.codeData)
	self.logger.info("write code " + self.file_path + " " + self.codeData)
        output.close()
        return {"result":True}

    @XBlock.json_handler
    def commit_to_git(self, data, suffix=''):
        """
        commit_to_git handler, which push code to gitlab.
        """
 	commit_message=data['commit_message']       
        student_id=self.runtime.anonymous_student_id
        real_user=self.runtime.get_real_user(self.runtime.anonymous_student_id)
	username = real_user.username
	email = real_user.email
	self.logger.info(username + " commit_to_gitlab " + commit_message)
        os.system("/edx/var/edxapp/staticfiles/xblock-script/pushToGit.sh "  + student_id + " " + username + " " + email + " " + commit_message)
        return {"result":True}






