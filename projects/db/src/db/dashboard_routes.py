import logging
from datetime import datetime
from http import HTTPStatus
from fastapi import APIRouter, Request, Path, Query
from starlette.responses import JSONResponse
from waspy.iba.file_handler import FileHandler


def add_dashboard_routes(router: APIRouter, file_name: str, dashboard_handler):
    """
    Adds API endpoints for dashboard functionality to the provided router.

    Args:
        router (APIRouter): The FastAPI router to add endpoints to.
        file_name (str): The base name for the dashboard files.
    """

    @router.get("/dashboard/current")
    async def latest_dashboard():
        """
        Returns the latest dashboard entry as a JSON response.
        If the file is not found, it returns a 404 error.
        """
        try:
            # Use JSONResponse to correctly format the output as JSON
            dashboard_data = dashboard_handler.get_dashboard()
            return JSONResponse(content=dashboard_data, status_code=HTTPStatus.OK)
        except FileNotFoundError:
            logging.warning(f"Dashboard file '{file_name}' not found.")
            return JSONResponse(
                content={"error": "Dashboard not found."},
                status_code=HTTPStatus.NOT_FOUND,
            )
        except Exception as e:
            logging.error(f"An unexpected error occurred: {e}", exc_info=True)
            return JSONResponse(
                content={"error": "An internal server error occurred."},
                status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            )

    @router.get("/dashboard/templates")
    async def get_templates():
        """
        Returns a list of all available template names.
        This endpoint aligns with the requested GET /api/templates structure.
        """
        try:
            template_names = dashboard_handler.get_template_names()
            return JSONResponse(content=template_names, status_code=HTTPStatus.OK)
        except Exception as e:
            logging.error(f"Failed to retrieve templates: {e}", exc_info=True)
            return JSONResponse(
                content={"error": f"Failed to retrieve templates. {e}"},
                status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            )

    @router.get("/dashboard/templates/{templateName}")
    async def get_template_by_name(templateName: str = Path(..., title="The name of the template")):
        """
        Returns a specific dashboard template by its name.
        This endpoint aligns with the requested GET /api/templates/{templateName} structure.
        """
        try:
            template_data = dashboard_handler.get_template(templateName)
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
        
    @router.get("/dashboard/endpoints")
    async def get_endpoints():
        try:
            dashboard_endpoints = dashboard_handler.get_endpoints()
            return JSONResponse(content=dashboard_endpoints, status_code=HTTPStatus.OK)
        except FileNotFoundError:
            logging.warning(f"dashboard-endpoints file was not found.")
            return JSONResponse(
                content={"error": f"dashboard-endpoints file was not found."},
                status_code=HTTPStatus.NOT_FOUND,
            )
        except Exception as e:
            logging.error(f"Failed to retrieve dashboard-endpoints: {e}", exc_info=True)
            return JSONResponse(
                content={"error": f"An internal server error occurred while retrieving the api dashboard-endpoints. {e}"},
                status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            )

    @router.post("/dashboard/save")
    async def save_dashboard(request: Request):
        """
        Saves the current dashboard entry to a timestamped file.
        The data is expected as a JSON body in the request.
        """
        try:
            dashboard_data = await request.json()
            
            dashboard_handler.save_dashboard(dashboard_data)


            logging.info(f"Dashboard entry saved.")
            return JSONResponse(
                content={"message": "Dashboard entry saved successfully."},
                status_code=HTTPStatus.CREATED
            )
        except Exception as e:
            logging.error(f"Failed to save dashboard entry: {e}", exc_info=True)
            return JSONResponse(
                content={"error": f"Failed to save dashboard entry. {e}"},
                status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            )
    
    @router.get("/dashboard/history/{identifier}")
    async def get_history_by_id(
        identifier: str,
        start: int = Query(None, description="Start timestamp in ms since epoch"),
        end: int = Query(None, description="End timestamp in ms since epoch"),
        limit: int = Query(100, description="Max number of entries to return"),
    ):
        """
        Returns entries of this identifier throughout the history of daybook,
        optionally filtered by time range.
        """
        try:
            return dashboard_handler.get_history_by_id(
                identifier=identifier,
                start=start,
                end=end,
                limit=limit
            )
        except Exception as e:
            logging.error(f"Failed to retrieve history of '{identifier}': {e}", exc_info=True)
            return JSONResponse(
                content={"error": f"An internal server error occurred while retrieving the history. {e}"},
                status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            )
    
    @router.post("/dashboard/add_to_favorites")
    async def add_to_favorites(request: Request):
        """
        Saves the current dashboard entry to a favorites file.
        The data is expected as a JSON body in the request.
        """
        try:
            dashboard_data = await request.json()
            
            dashboard_handler.add_to_favorites(dashboard_data)


            logging.info(f"Dashboard added to favorites.")
            return JSONResponse(
                content={"message": "Dashboard entry saved successfully."},
                status_code=HTTPStatus.CREATED
            )
        except Exception as e:
            logging.error(f"Failed to save dashboard entry as favorites: error={e}", exc_info=True)
            return JSONResponse(
                content={"error": f"Failed to save dashboard entry as favorites. error={e}"},
                status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            )