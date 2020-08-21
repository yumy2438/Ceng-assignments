#include "Light.h"
#include<cmath>
/* Constructor. Implemented for you. */
PointLight::PointLight(const Vector3f & position, const Vector3f & intensity)
    : position(position), intensity(intensity)
{
}

// Compute the contribution of light at point p using the
// inverse square law formula
Vector3f PointLight::computeLightContribution(const Vector3f& p)
{
	Vector3f diff=sub(position,p);
	float diffe=dot_product(diff,diff);
	Vector3f returning;
	returning.x=intensity.x/diffe;
	returning.y=intensity.y/diffe;
	returning.z=intensity.z/diffe;
	return returning;
	/***********************************************
     *                                             *
	 * TODO: Implement this function               *
     *                                             *
     ***********************************************
	 */
}
