#version 410

layout(location = 0) in vec3 position;

// Data from CPU
uniform mat4 MVP; // ModelViewProjection Matrix
uniform mat4 MV; // ModelView idMVPMatrix
uniform vec4 cameraPosition;
uniform vec3 lightPosition;
uniform float heightFactor;
uniform int leftrightamount;

// Texture-related data
uniform sampler2D tex0;
uniform sampler2D tex1;
uniform int widthTexture;
uniform int heightTexture;


// Output to Fragment Shader
out vec2 textureCoordinate; // For texture-color
out vec3 vertexNormal; // For Lighting computation
out vec3 ToLightVector; // Vector from Vertex to Light;
out vec3 ToCameraVector; // Vector from Vertex to Camera;

void main()
{

    // get texture value, compute height
    vec3 pos = position;

    textureCoordinate=vec2(1,1)-vec2((position.x-leftrightamount)/widthTexture,position.z/heightTexture);
    vec3 heightColor=texture(tex1,textureCoordinate).xyz;
    pos.y=heightFactor*heightColor.x;



    // compute normal vector using also the heights of neighbor vertices
    vec2 nTC=vec2(1,1)-vec2(((position.x-leftrightamount)-1)/widthTexture,(position.z)/heightTexture);
    vec3 hC=texture(tex1,nTC).xyz;
    vec3 n1=vec3(position.x-1,heightFactor*hC.x,position.z);
    n1=n1-pos;
    
    nTC=vec2(1,1)-vec2(((position.x-leftrightamount)-1)/widthTexture,(position.z+1)/heightTexture);
    hC=texture(tex1,nTC).xyz;
    vec3 n2=vec3(position.x-1,heightFactor*hC.x,position.z+1);
    n2=n2-pos;

    nTC=vec2(1,1)-vec2(((position.x-leftrightamount))/widthTexture,(position.z+1)/heightTexture);
    hC=texture(tex1,nTC).xyz;
    vec3 n3=vec3(position.x,heightFactor*hC.x,position.z+1);
n3=n3-pos;

    nTC=vec2(1,1)-vec2(((position.x-leftrightamount)+1)/widthTexture,(position.z)/heightTexture);
    hC=texture(tex1,nTC).xyz;
    vec3 n4=vec3(position.x+1,heightFactor*hC.x,position.z);
n4=n4-pos;

    nTC=vec2(1,1)-vec2(((position.x-leftrightamount)+1)/widthTexture,(position.z-1)/heightTexture);
    hC=texture(tex1,nTC).xyz;
    vec3 n5=vec3(position.x+1,heightFactor*hC.x,position.z-1);
n5=n5-pos;
    nTC=vec2(1,1)-vec2(((position.x-leftrightamount))/widthTexture,(position.z-1)/heightTexture);
    hC=texture(tex1,nTC).xyz;
    vec3 n6=vec3(position.x,heightFactor*hC.x,position.z-1);
n6=n6-pos;
    // compute normal vector using also the heights of neighbor vertices

        vertexNormal = normalize(cross(n1, n2) + cross(n2, n3) + cross(n3, n4) + cross(n4, n5)
                            + cross(n5, n6) + cross(n6, n1));

    
    ToCameraVector = normalize(cameraPosition.xyz - pos);
    ToLightVector = normalize(lightPosition - pos);

    gl_Position = MVP * vec4(pos, 1.0);

}
