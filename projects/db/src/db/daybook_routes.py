import logging
from datetime import datetime
from http import HTTPStatus
from fastapi import APIRouter, Request, Path
from starlette.responses import JSONResponse
from waspy.iba.file_handler import FileHandler


def add_daybook_routes(router: APIRouter, file_handler: FileHandler, file_name: str):
    """
    Adds API endpoints for daybook functionality to the provided router.

    Args:
        router (APIRouter): The FastAPI router to add endpoints to.
        file_handler (FileHandler): An instance of the file handler for data access.
        file_name (str): The base name for the daybook files.
    """

    @router.get("/daybook/current")
    async def latest_daybook():
        """
        Returns the latest daybook entry as a JSON response.
        If the file is not found, it returns a 404 error.
        """
        try:
            # Use JSONResponse to correctly format the output as JSON
            daybook_data = file_handler.get_daybook()
            return JSONResponse(content=daybook_data, status_code=HTTPStatus.OK)
        except FileNotFoundError:
            logging.warning(f"Daybook file '{file_name}' not found.")
            return JSONResponse(
                content={"error": "Daybook not found."},
                status_code=HTTPStatus.NOT_FOUND,
            )
        except Exception as e:
            logging.error(f"An unexpected error occurred: {e}", exc_info=True)
            return JSONResponse(
                content={"error": "An internal server error occurred."},
                status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            )

    @router.get("/daybook/templates")
    async def get_templates():
        """
        Returns a list of all available template names.
        This endpoint aligns with the requested GET /api/templates structure.
        """
        try:
            # Assuming file_handler has a method to list available templates
            template_names = file_handler.get_template_names()
            return JSONResponse(content=template_names, status_code=HTTPStatus.OK)
        except Exception as e:
            logging.error(f"Failed to retrieve templates: {e}", exc_info=True)
            return JSONResponse(
                content={"error": f"Failed to retrieve templates. {e}"},
                status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            )

    @router.get("/daybook/templates/{templateName}")
    async def get_template_by_name(templateName: str = Path(..., title="The name of the template")):
        """
        Returns a specific daybook template by its name.
        This endpoint aligns with the requested GET /api/templates/{templateName} structure.
        """
        try:
            # Assuming file_handler has a method to get a specific template by name
            template_data = file_handler.get_template(templateName)
            return JSONResponse(content=template_data, status_code=HTTPStatus.OK)
        except FileNotFoundError:
            logging.warning(f"Template '{templateName}' not found.")
            return JSONResponse(
                content={"error": f"Template '{templateName}' not found."},
                status_code=HTTPStatus.NOT_FOUND,
            )
        except Exception as e:
            logging.error(f"Failed to retrieve template '{templateName}': {e}", exc_info=True)
            return JSONResponse(
                content={"error": f"An internal server error occurred while retrieving the template. {e}"},
                status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            )
        
    @router.get("/daybook/endpoints")
    async def get_daybook_endpoints():
        try:
            daybook_endpoints = file_handler.get_daybook_endpoints()
            return JSONResponse(content=daybook_endpoints, status_code=HTTPStatus.OK)
        except FileNotFoundError:
            logging.warning(f"daybook-endpoints file was not found.")
            return JSONResponse(
                content={"error": f"daybook-endpoints file was not found."},
                status_code=HTTPStatus.NOT_FOUND,
            )
        except Exception as e:
            logging.error(f"Failed to retrieve daybook-endpoints: {e}", exc_info=True)
            return JSONResponse(
                content={"error": f"An internal server error occurred while retrieving the api daybook-endpoints. {e}"},
                status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            )

    @router.post("/daybook/save")
    async def save_daybook(request: Request):
        """
        Saves the current daybook entry to a timestamped file.
        The data is expected as a JSON body in the request.
        """
        try:
            daybook_data = await request.json()
            
            # Generate a unique, timestamped filename
            timestamp = datetime.now().strftime("%Y-%m-%d")
            filename = f"daybook_{timestamp}.json"
            
            # Save the data using the file handler
            file_handler.save_daybook(daybook_data, filename)

            logging.info(f"Daybook entry saved as '{filename}'.")
            return JSONResponse(
                content={"message": "Daybook entry saved successfully.", "filename": filename},
                status_code=HTTPStatus.CREATED
            )
        except Exception as e:
            logging.error(f"Failed to save daybook entry: {e}", exc_info=True)
            return JSONResponse(
                content={"error": f"Failed to save daybook entry. {e}"},
                status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            )
