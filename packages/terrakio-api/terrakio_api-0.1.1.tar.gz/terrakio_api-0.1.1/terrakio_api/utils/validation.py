from typing import Dict, Any, List
from ..exceptions import ValidationError

def validate_feature(feature: Dict[str, Any]) -> None:
    """
    Validate a GeoJSON Feature object.
    
    Args:
        feature: GeoJSON Feature dictionary
        
    Raises:
        ValidationError: If the feature is invalid
    """
    if not isinstance(feature, dict):
        raise ValidationError("Feature must be a dictionary")
    
    if feature.get('type') != 'Feature':
        raise ValidationError("Feature must have 'type' property set to 'Feature'")
    
    if 'geometry' not in feature:
        raise ValidationError("Feature must have a 'geometry' property")
    
    geometry = feature['geometry']
    if not isinstance(geometry, dict):
        raise ValidationError("Feature geometry must be a dictionary")
    
    if 'type' not in geometry:
        raise ValidationError("Geometry must have a 'type' property")
    
    if 'coordinates' not in geometry:
        raise ValidationError("Geometry must have a 'coordinates' property")
    
    # Add more specific validation based on geometry type if needed

def create_point_feature(lon: float, lat: float, properties: Dict[str, Any] = None) -> Dict[str, Any]:
    """
    Create a GeoJSON Point Feature object.
    
    Args:
        lon: Longitude coordinate
        lat: Latitude coordinate
        properties: Optional properties dictionary (default: empty dict)
        
    Returns:
        Dict: GeoJSON Feature object
    """
    if properties is None:
        properties = {}
        
    return {
        "type": "Feature",
        "properties": properties,
        "geometry": {
            "type": "Point",
            "coordinates": [lon, lat]
        }
    }


def create_polygon_feature(coordinates: List[List[float]], properties: Dict[str, Any] = None) -> Dict[str, Any]:
    """
    Create a GeoJSON Polygon Feature object.
    
    Args:
        coordinates: List of [lon, lat] coordinate pairs forming a polygon (first and last must be identical)
        properties: Optional properties dictionary (default: empty dict)
        
    Returns:
        Dict: GeoJSON Feature object
    """
    if properties is None:
        properties = {}
    
    # Check if polygon is closed
    if coordinates[0] != coordinates[-1]:
        coordinates.append(coordinates[0])  # Close the polygon
        
    return {
        "type": "Feature",
        "properties": properties,
        "geometry": {
            "type": "Polygon",
            "coordinates": [coordinates]
        }
    }