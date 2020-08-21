#include "defs.h"
#include <cmath>

float dot_product(const Vector3f& v1, const Vector3f& v2){
	return v1.x*v2.x+v1.y*v2.y+v1.z*v2.z;
}
Vector3f cross_product(const Vector3f& v1, const Vector3f& v2){
	Vector3f vCrossProduct;
	float v1x = v1.x;
	float v1y = v1.y;
	float v1z = v1.z;
	float v2x = v2.x;
	float v2y = v2.y;
	float v2z = v2.z;
	vCrossProduct.x = v1y * v2z - v1z * v2y;
    vCrossProduct.y = v1.z * v2x - v1x * v2z;
    vCrossProduct.z = v1x * v2y - v1y * v2x;
    return vCrossProduct;
}
Vector3f sum(const Vector3f& v1, const Vector3f& v2){
	Vector3f returning;
	returning.x=v1.x+v2.x;
	returning.y=v1.y+v2.y;
	returning.z=v1.z+v2.z;
	return returning;
}
Vector3f ikili(const Vector3f& v1, const Vector3f& v2){
	Vector3f returning;
	returning.x=v1.x*v2.x;
	returning.y=v1.y*v2.y;
	returning.z=v1.z*v2.z;
	return returning;
}
Vector3f sub(const Vector3f& v1, const Vector3f& v2){
	Vector3f returning;
	returning.x=v1.x-v2.x;
	returning.y=v1.y-v2.y;
	returning.z=v1.z-v2.z;
	return returning;

}
Vector3f scalar_product(const Vector3f& v1, float t){
	Vector3f returning;
	returning.x=v1.x*t;
	returning.y=v1.y*t;
	returning.z=v1.z*t;
	return returning;
}
float det(const Vector3f& v1, const Vector3f& v2, const Vector3f& v3){
	return v1.x*v2.y*v3.z+v2.x*v3.y*v1.z+v3.x*v1.y*v2.z-v3.x*v2.y*v1.z-v3.y*v2.z*v1.x-v3.z*v2.x*v1.y;
}
Vector3f normalize(const Vector3f& v)
{
	Vector3f returning;
	float x = v.x;
	float y = v.y;
	float z = v.z;
	float len = sqrt(x*x+y*y+z*z);
	returning.x = x/len;
	returning.y = y/len;
	returning.z = z/len;
	return returning;
}