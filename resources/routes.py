from resources.auth import RegisterResource, LoginResource
from resources.complaint import ComplaintsResource, ComplaintApproveResource, ComplaintRejectResource, ComplaintResource

routes = (
    (RegisterResource, '/register'),
    (LoginResource, '/login'),
    (ComplaintsResource, '/complaints'),
    (ComplaintResource, '/complaints/<int:pk>'),

    (ComplaintApproveResource, '/complaints/<int:pk>/approve'),
    (ComplaintRejectResource, '/complaints/<int:pk>/reject'),
)
