#ifndef _DEFS_H_
#define _DEFS_H_

class Scene;


/* 3 dimensional vector holding floating point numbers.
Used for both coordinates and color. 
Use x, y, z for coordinate computations, and use r, g, b for color computations. 
Note that you do not have to use this one if you use any vector computation library like Eigen. */
typedef struct Vector3f
{
	union 
	{
		float x;
		float r;
	};
	union
	{
		float y;
		float g;
	};
	union
	{
		float z;
		float b;
	};
} Vector3f;

/* Structure to hold return value from ray intersection routine. 
This should hold information related to the intersection point, 
for example, coordinate of the intersection point, surface normal at the intersection point etc. 
Think about the variables you will need for this purpose and declare them here inside of this structure. */
typedef struct ReturnVal
{
	float t;
	bool is_intersected;
	Vector3f intersection_point;
	Vector3f surface_normal;
	Vector3f cam_pos;
	/***********************************************
     *                                             *
	 * TODO: Implement this structure              *
     *                                             *
     ***********************************************
	 */
} ReturnVal;
float dot_product(const Vector3f& v1, const Vector3f& v2);
Vector3f cross_product(const Vector3f& v1, const Vector3f& v2);
Vector3f sum(const Vector3f& v1, const Vector3f& v2);
Vector3f sub(const Vector3f& v1, const Vector3f& v2);
Vector3f ikili(const Vector3f& v1, const Vector3f& v2);
Vector3f scalar_product(const Vector3f& v1, float t);
float det(const Vector3f& v1, const Vector3f& v2, const Vector3f& v3);
Vector3f normalize(const Vector3f& v);
//
// The global variable through which you can access the scene data
//
extern Scene* pScene;

#endif
