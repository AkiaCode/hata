__all__ = ('IntegrationDetail', )

from ..utils import timestamp_to_datetime, DISCORD_EPOCH_START
from ..role import create_partial_role_from_id

from .preinstanced import IntegrationExpireBehavior

class IntegrationDetail:
    """
    Details about a non discord integration.
    
    Attributes
    ----------
    expire_behavior : ``IntegrationExpireBehavior``
        The behavior of expiring subscription.
    expire_grace_period : `int`
        The grace period in days for expiring subscribers. Can be `1`, `3`, `7`, `14` or `30`. If the integration is
        partial, or is not applicable for it, then is set as `-1`.
    role : `None` or ``Role``
        The role what the integration uses for subscribers.
    subscriber_count : `int`
        How many subscribers the integration has. Defaults to `0`.
    synced_at : `datetime`
        When the integration was last synced.
    syncing : `bool`
        Whether the integration syncing.
    """
    __slots__ = ('expire_behavior', 'expire_grace_period', 'role', 'subscriber_count', 'synced_at', 'syncing', )
    
    def __init__(self, data):
        """
        Fills up the integration detail from the respective integration's data.
        
        Parameters
        ----------
        data : `dict` of (`str`, `Any`) items
            Received integration data.
        """
        self.syncing = data.get('syncing', False)
        
        role_id = data.get('role_id', None)
        if role_id is None:
            role = None
        else:
            role = create_partial_role_from_id(int(role_id))
        self.role = role
        
        self.expire_behavior = IntegrationExpireBehavior.get(data.get('expire_behavior', 0))
        
        self.expire_grace_period = data.get('expire_grace_period', -1)
        
        try:
            synced_at = data['synced_at']
        except KeyError:
            synced_at = DISCORD_EPOCH_START
        else:
            synced_at = timestamp_to_datetime(synced_at)
        self.synced_at = synced_at
        
        self.subscriber_count = data.get('subscriber_count', 0)
    
    @classmethod
    def from_role(cls, role):
        """
        Creates a partial integration detail with the given role.
        
        Parameters
        ----------
        role : ``Role``
            The respective role.
        
        Returns
        -------
        self : ``IntegrationDetail``
            The created integration detail.
        """
        self = object.__new__(cls)
        self.syncing = False
        self.role = role
        self.expire_behavior = IntegrationExpireBehavior.remove_role
        self.expire_grace_period = -1
        self.synced_at = DISCORD_EPOCH_START
        self.subscriber_count = 0
        return self
    
    def __repr__(self):
        """Returns the integration detail's representation."""
        return f'<{self.__class__.__name__} role={self.role!r}>'
