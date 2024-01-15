from resources.auth import RegisterResource, LoginResource
from resources.complaint import ComplaintsResource, ComplaintApproveResource, ComplaintRejectResource

routes = (
    (RegisterResource, '/register'),
    (LoginResource, '/login'),
    (ComplaintsResource, '/complaints'),
    # TODO: new URL for single complaint

    (ComplaintApproveResource, '/complaints/<int:pk>/approve'),
    (ComplaintRejectResource, '/complaints/<int:pk>/reject'),
)
