#!/usr/bin/env python
import rospy
from nour_behave.srv import ServiceExample,ServiceDetect
import signal
import os,sys,inspect
current_dir= os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir= os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)
import dialogflow_client

def print_context_parameters(contexts):
    result = []
    for context in contexts:
        param_list = []
        temp_str = '\n\t'
        for parameter in context.parameters:
            param_list.append("{}: {}".format(
                    parameter, context.parameters[parameter]))
        temp_str += "Name: {}\n\tParameters:\n\t {}".format(
                context.name.split('/')[-1], "\n\t".join(param_list))
        result.append(temp_str)
    result = "\n".join(result)
    return result


def print_parameters(parameters):
    param_list = []
    temp_str = '\n\t'
    for parameter in parameters:
        param_list.append("{}: {}\n\t".format(
                parameter, parameters[parameter]))
        temp_str += "{}".format("\n\t".join(param_list))
        return temp_str

# Extract the plain parameter for the address
def getAddress(parameters):
    temp_str = ''
    for parameter in parameters:
        temp_str += "{}".format(parameters[parameter])
        return temp_str

def print_result(result):
    output = "DF_CLIENT: Results:\n" \
             "Query Text: {}\n" \
             "Detected intent: {} (Confidence: {})\n" \
             "Contexts: {}\n" \
             "Fulfillment text: {}\n" \
             "Action: {}\n" \
             "Parameters: {}".format(
                     result.query_text,
                     result.intent.display_name,
                     result.intent_detection_confidence,
                     print_context_parameters(result.output_contexts),
                     result.fulfillment_text,
                     result.action,
                     print_parameters(result.parameters))
    return output

#Check actions at each response
def checkAction(result):
    if result.action == 'map.navi':
        try:
            srv= rospy.ServiceProxy('/nour_naviagte', ServiceExample)
            serviceRes= srv(getAddress(result.parameters))
            print("{} service called...".format(result.action))
            print("Service Response:")
            print(serviceRes)
        except rospy.ServiceException as e:
            print("Service call failed: %s"%e)

    elif result.action == 'MoveCommand':
        try:
            srv= rospy.ServiceProxy('/nour_naviagte', ServiceExample)
            serviceRes= srv(getAddress(result.parameters))
            print("{} service called...".format(result.action))
            print("Service Response:")
            print(serviceRes)
        except rospy.ServiceException as e:
            print("Service call failed: %s"%e)

    elif result.action == 'ChangeVoice':
        rospy.set_param('accent_voice',getAddress(result.parameters))
        print("Changed Voice to "+ getAddress(result.parameters))
        #rospy.sleep()
        os.system('python -c "exit()" && gnome-terminal -- roslaunch dialogflow_ros hotword_df.launch && gnome-terminal -- rostopic pub -1 /dialogflow_client/requests/string_msg std_msgs/String "Changed-Voice-To English UK"')
        # Remove the message then make it a custom intent that triggers in this line
        print('Restarting System...')
        df = dialogflow_client.DialogflowClient()
        df.exit()

    elif result.action == 'StartVisionDetect':
        try:
            srv= rospy.ServiceProxy('/nour_detect', ServiceDetect)
            serviceRes= srv(result.action)
            print("{} service called...".format(result.action))
            print("Service Response:")
            print(serviceRes)
        except rospy.ServiceException as e:
            print("Service call failed: %s"%e)

    else:
        print("No movement actions to take.")
        
    
