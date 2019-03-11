# coding:utf-8

# author: s0nnet
# time: 2016-11-28
# desc: urls

from viewset.view_login import *
from viewset.view_index import *
from viewset.view_user import *
from viewset.view_service import *
from viewset.view_abtest import *
from viewset.view_myproject import *
from viewset.view_dashboard import *
from viewset.view_algostar import *
from viewset.view_tagService import *
from viewset.view_service_QAmsg import *
from viewset.view_abjsClient import *
from viewset.view_service_cli import *
urls = (
    "/", ViewIndex,
    "/index", ViewIndex,
    "/indexTest.html",ViewABjsClient,
    "/wizard-create-profile.html",Viewwizard,
    "/index.html", ViewIndex,
    "/web_app.html",ViewLandingPage,
    "/abtest.html", ViewAbtest,
    "/my_abexp.html", ViewMyAbExp,
    "/my_abexpAdd.html",viewMyAbexpAdd,
    "/abtest_create.html",ViewAbtestCreate,
    "/name=(.*)", ViewExpdetails,
    "/tags/tag=(.*)", ViewTagService,
    "/expdetails.html", ViewExpdetails,
    "/my_project_main.html", ViewMyProject,
    "/service_zoo_list.html", ViewAlgoZooList,
    "/service_add.html", ViewAlgoAdd,
    "/service_list.html", ViewAlgoList,
    "/username=(.*)&;projectname=(.*)", ViewAlgoDetails,
    "/services/username=(.*)", ViewOtherProject,
    "/user_list.html", ViewUserList,
    "/user_add.html", ViewUserAdd,
    "/user_edit.html", ViewUserEdit,
    "/user_grade.html",ViewUserGrade,
    "/login", ViewLogin,
    "/profile.html", ViewIProfile,
    "/logout", ViewLogout,
    "/api/users/me",ViewApiMeInfo,
    "/api/data/count", ViewApiDataCount,
    "/api/dashboard/index",ViewApiDashboardIndex,
    "/api/service/algo_deploy",ViewApiAlgoPublish,
    "/api/service/algo_undeploy",ViewApiAlgoUnpublish,
    "/api/service/user/list", ViewApiServUserList,
    "/api/service/user/add", ViewApiServUserAdd,
    "/api/service/msg/save",ViewApiQAMsgSave,
    "/api/service/msg/query",ViewApiQAdata,
    "/api/service/request",ViewApiServiceCli,
    #"/api/service/msg/user",ViewApiServMsgUser,
    #"/api/service/msg/list",ViewApiServMsgList,
    "/api/service/runapi",ViewApiRunApi,
    "/api/service/algolist",ViewApiServList,
    #"/api/service/algostarget",ViewApiAlgoStarGet,
    "/api/service/algostarupdate",ViewApiAlgoStarUpdate,
    "/api/service/staredinfo",ViewApiStaredInfo,
    "/api/user/list", ViewApiUserList,
    "/api/user/add", ViewApiUserAdd,
    "/api/user/info", ViewApiUserInfo,
    "/api/user/update", ViewApiUserUpdate,
    "/api/user/del", ViewApiUserDel,
    "/api/abtest/add",ViewApiAbtestAdd,
    "/api/abtest/abservlist",ViewApiAbServList,
    "/api/abtest/zooablist",ViewApiabZooList,#abzoo
    "/api/abtest/myablist",ViewApiMyAbList,
    "/api/abtest/myabdetails",ViewApiMyAbDetails,#abtest 详情页
    "/api/abtest/abactions",ViewApiAbActions,#abtest实验设置
)
