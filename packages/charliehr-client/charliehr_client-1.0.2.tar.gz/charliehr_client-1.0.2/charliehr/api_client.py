import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry


class CharlieHRClient:
########################################################################################################################
# INTERNAL METHODS
########################################################################################################################
    def __init__(self, client_id: str, client_secret: str, timeout=10, max_retries=3, backoff_factor=0.3) -> None:
        """
        Initialise the API client and set default attributes
        :param client_id: Can be obtained from the CharlieHR platform
        :param client_secret: Can be obtained from the CharlieHR platform
        :param timeout: Set to 10 seconds as the default
        :param max_retries: Will attempt 3 requests before returning an error
        :param backoff_factor: Exponential backoff. Increase to extend the time between retries. 0.3 is the default
        """
        self.base_url = "https://charliehr.com/api/v1/"
        self.client_id = client_id
        self.client_secret = client_secret
        self.timeout = timeout
        self.session = self._init_session(max_retries, backoff_factor)

########################################################################################################################
    @staticmethod
    def _init_session(max_retries: int, backoff_factor: float) -> requests.Session():
        """
         Configure a requests session with retries.
        :param max_retries: Maximum number of retries. Defaults to 3.
        :param backoff_factor: Backoff factor for retries. Defaults to 0.3.
        :return: Requests Session
        """
        session = requests.Session()
        retries = Retry(
            total=max_retries,
            backoff_factor=backoff_factor,
            status_forcelist=[429, 500, 502, 503, 504],
            allowed_methods=["HEAD", "GET", "OPTIONS", "POST", "PUT", "DELETE"]
        )
        adapter = HTTPAdapter(max_retries=retries)
        session.mount('http://', adapter)
        session.mount('https://', adapter)
        return session

########################################################################################################################
    def _get_auth_headers(self, method: str) -> dict:
        """
        Return the authorization headers required for API requests.
        :return: dict: Authorization header
        """
        token = f"Token token={self.client_id}:{self.client_secret}"
        headers = {"Authorization": token}
        if method == "POST":
            headers['Content-Type'] = "application/json"
        return headers

########################################################################################################################
    def _build_url(self, base_endpoint: str, next_url: str) -> str:
        """
        Build the full request URL based on the next page information.
        :param base_endpoint: The base API endpoint.
        :param next_url: The next page query string.
        :return: Full URL for the next request.
        """
        if next_url.startswith('?'):
            return f"{self.base_url}/{base_endpoint}{next_url}"
        return f"{self.base_url}/{next_url.lstrip('/')}"

########################################################################################################################
    def _handle_response(self, response: requests.models.Response) -> dict:
        """
         Validate and parse the HTTP response.
        :param response: HTTP response
        :return: dict: Parsed JSON response.
        :raise: Exception: If the response indicates an error.
        """
        try:
            response.raise_for_status()
            return response.json()
        except requests.exceptions.Timeout:
            raise Exception(f"Request to {response.url} timed out after {self.timeout} seconds.")
        except requests.exceptions.HTTPError as http_err:
            raise Exception(f"HTTP error occurred: {http_err} - Response: {response.text}")
        except requests.exceptions.RequestException as err:
            raise Exception(f"Error during request: {err}")

########################################################################################################################
    def __request(self, method: str, endpoint: str, **kwargs) -> [list, dict]:
        """
        Perform an HTTP request and handle pagination if necessary.
        :param method: HTTP method (GET, POST, PUT, DELETE).
        :param endpoint: API endpoint.
        :param kwargs: Additional arguments for the request.
        :return: list or dict: Aggregated paginated data or a single dictionary response.
        """
        all_data = []
        next_url = endpoint
        base_endpoint = endpoint.lstrip('/').split('?')[0]

        while next_url:
            url = self._build_url(base_endpoint, next_url)
            headers = kwargs.pop("headers", {})
            headers.update(self._get_auth_headers(method))
            response = self.session.request(method, url, timeout=self.timeout, headers=headers, **kwargs)
            print(type(response))
            json_response = self._handle_response(response)

            if not json_response.get('success') or 'data' not in json_response:
                break

            data = json_response['data']

            if isinstance(data, list):
                all_data.extend(data)
                next_url = json_response.get('meta', {}).get('next_url')
            elif isinstance(data, dict):
                return data
            else:
                break

        return all_data

########################################################################################################################
# PUBLIC METHODS
########################################################################################################################
    def get_all_bank_accounts(self) -> list:
        """
        :return: List with bank account information for all team members of the authenticated company.
        """
        return self.__request("GET", "/bank_accounts/")
########################################################################################################################
    def get_all_offices(self) -> list:
        """
        :return: List containing all offices associated with the company.
        """
        return self.__request("GET", "/offices/")
########################################################################################################################
    def get_all_employees(self) -> list:
        """
        :return: List of all employees in the company.
        """
        return self.__request("GET", "/team_members/")
########################################################################################################################
    def get_all_salaries(self) -> list:
        """
        :return: List of all employee salaries.
        """
        return self.__request("GET", "/salaries/")
########################################################################################################################
    def get_all_note_types(self) -> list:
        """
        :return: List of all note types
        """
        return self.__request("GET", "/team_member_note_types/")
########################################################################################################################
    def get_all_teams(self) -> list:
        """
        :return: List of all teams.
        """
        return self.__request("GET", "/teams/")
########################################################################################################################
    def get_company_details(self) -> dict:
        """
        :return: Dictionary of company information.
        """
        return self.__request("GET", "/company/")
########################################################################################################################
    def get_office_details(self, office_id: str) -> dict:
        """
        :param: office_id: UUID of the office
        :return: Dictionary containing details of the specified office.
        """
        return self.__request("GET", f"/offices/{office_id}")
########################################################################################################################
    def get_employee_bank_account(self, employee_id: str) -> dict:
        """
        :param: user_id: UUID of the employee.
        :return: Dictionary with a single bank account for the specified employee.
        """
        return self.__request("GET", f"/bank_accounts/{employee_id}")
########################################################################################################################
    def get_employee_details(self, employee_id: str) -> dict:
        """
        :param: user_id: UUID of the employee.
        :return: Dictionary containing details for the specified employee.
        """
        return self.__request("GET", f"/team_members/{employee_id}")
########################################################################################################################
    def get_employee_salary(self, employee_id: str) -> dict:
        """
        :param employee_id: UUID of the employee.
        :return: Dictionary containing employee salary information.
        """
        return self.__request("GET", f"/team_members/{employee_id}/salaries/")
########################################################################################################################
    def get_employee_leave_allowance(self, employee_id: str) -> dict:
        """
        :param employee_id: UUID of the employee.
        :return: Dictionary containing employee PTO Balance.
        """
        return self.__request("GET", f"/team_members/{employee_id}/leave_allowance/")
########################################################################################################################
    def get_employee_leave_requests(self, employee_id: str) -> dict:
        """
        :param employee_id: UUID of the employee.
        :return: Dictionary containing employee leave requests.
        """
        return self.__request("GET", f"/team_members/{employee_id}/leave_requests/")
########################################################################################################################
    def get_employee_notes(self, employee_id: str) -> list:
        """
        :param employee_id: UUID of the employee.
        :return: List of all note types.
        """
        return self.__request("GET", f"/team_members/{employee_id}/notes")
########################################################################################################################
    def get_note_type_details(self, note_type_id: str) -> dict:
        """
        :param: note_type_id: UUID of the note type.
        :return: Dictionary containing note type information
        """
        return self.__request("GET", f"/team_member_note_types/{note_type_id}")
########################################################################################################################
    def get_team_details(self, team_id: str) -> dict:
        """
        :param: team_id: UUID of the team.
        :return: Dictionary containing team information.
        """
        return self.__request("GET", f"/teams/{team_id}")
########################################################################################################################
    def create_note_type(self, name: str, note_type: str, anyone=False, owners=True, team_leads=True, line_managers=True,
                         payroll_admins=True, admins=True, super_admins=True) -> dict:
        """
        :param name: Name of the new note type to create
        :param note_type: Data Type: Choose from the following: (Text, Number or Checklist)
        :param anyone: Permissions to amend the value. Default value is False.
        :param owners: Permissions to amend the value. Default value is True.
        :param team_leads: Permissions to amend the value. Default value is True.
        :param line_managers: Permissions to amend the value. Default value is True.
        :param payroll_admins: Permissions to amend the value. Default value is True.
        :param admins: Permissions to amend the value. Default value is True.
        :param super_admins: Permissions to amend the value. Default value is True.
        :return: Dictionary containing details of the new note type which was created
        """
        data = {'name': name,
                'type':note_type,
                'permissions':
                    {
                        'anyone': anyone,
                        'owners': owners,
                        'team_leads': team_leads,
                        'line_managers': line_managers,
                        'payroll_admins': payroll_admins,
                        'admins': admins,
                        'super_admins': super_admins
                    }
                }
        return self.__request("POST", f"/team_member_note_types/", json=data)

########################################################################################################################
    def create_employee_note(self, employee_id: str, note_id: str, content: str) -> dict:
        """
        :return: Dictionary containing details of the note which was created.
        """
        data = {'team_member_note_type_id': note_id, 'content': content}
        return self.__request("POST", f"/team_members/{employee_id}/notes", json=data)
########################################################################################################################
# END
########################################################################################################################
