import requests

TICKET_APP_ID = "50";

API_ADDR = "/SBTDWebApi/api"
BASE_URL = "https://[removed].teamdynamix.com"

TICKET_UI_URL = BASE_URL + "/SBTDNext/Apps/" + TICKET_APP_ID + "/Tickets/TicketDet?TicketID="

Url = {
	"NEW_TICKET": BASE_URL + API_ADDR + "/" + TICKET_APP_ID + "/tickets/",
	"FIND_UID": BASE_URL + API_ADDR + "/people/lookup/"
}

# params:
#	data: The object containing the original request's data
#
# returns: The message that will be sent to the user after attempting to create a ticket
def newTicket(data):
	command_args = data["text"].split()
	requestor = command_args[0]
	title = getTitle(command_args)

	try:
		requestorUID = uniqueIDToUID(requestor)
	except:
		return "Invalid uniqueID."

	headers = {"Authorization": ("Bearer " + mrRobotAuth())}
	body = {
		"TypeID": 6794,
		"Title": title,
		"AccountID": 20050,
		"StatusID": 1081,
		"PriorityID": 1925,
		"RequestorUid": requestorUID
	}

	params = {
		"EnableNotifyReviewer": False,
		"NotifyRequestor": False,
		"NotifyResponsible": True,
		"AllowRequestorCreation": False
	}

	response = requests.post(Url["NEW_TICKET"], headers=headers, data=body, params=params)
	json = response.json()

	if response.status_code < 200 or response.status_code > 299:
		print(json)
		return "An error occurred - check console for details"

	else:
		return "Ticket successfully created: " + TICKET_UI_URL + str(json["ID"])


# params:
#	uniqueID: User's uniqueID
#
# returns:	TeamDynamix UID (String)
def uniqueIDToUID(uniqueID):
	headers = {"Authorization": ("Bearer " + mrRobotAuth())}
	params = { "searchText": uniqueID, "maxResults": 1 }

	response = requests.get(Url["FIND_UID"], headers=headers, params=params)

	return response.json()[0]["UID"]

# returns:	JWT auth token
def mrRobotAuth():
	body = {
		"username": "[removed]",
		"password": "[removed]"
	}

	response = requests.post(BASE_URL + "/TDWebApi/api/auth", data=body)
	return response.content.decode('UTF-8')


# params:
#	args: The arguments for the create ticket command in split() form
#
# returns: the title of the new ticket as specified in the command's arguments
def getTitle(args):
	first = True
	cat = ""

	for string in args:
		if first:
			first = False
			continue
		else:
			cat += string + " "

	return cat