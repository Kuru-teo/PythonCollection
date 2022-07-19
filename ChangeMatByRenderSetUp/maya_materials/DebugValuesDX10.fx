/*********************************************************************NVMH3****
*******************************************************************************
$Revision: #2 $

Copyright NVIDIA Corporation 2008
TO THE MAXIMUM EXTENT PERMITTED BY APPLICABLE LAW, THIS SOFTWARE IS PROVIDED
*AS IS* AND NVIDIA AND ITS SUPPLIERS DISCLAIM ALL WARRANTIES, EITHER EXPRESS
OR IMPLIED, INCLUDING, BUT NOT LIMITED TO, IMPLIED WARRANTIES OF MERCHANTABILITY
AND FITNESS FOR A PARTICULAR PURPOSE.  IN NO EVENT SHALL NVIDIA OR ITS SUPPLIERS
BE LIABLE FOR ANY SPECIAL, INCIDENTAL, INDIRECT, OR CONSEQUENTIAL DAMAGES
WHATSOEVER (INCLUDING, WITHOUT LIMITATION, DAMAGES FOR LOSS OF BUSINESS PROFITS,
BUSINESS INTERRUPTION, LOSS OF BUSINESS INFORMATION, OR ANY OTHER PECUNIARY
LOSS) ARISING OUT OF THE USE OF OR INABILITY TO USE THIS SOFTWARE, EVEN IF
NVIDIA HAS BEEN ADVISED OF THE POSSIBILITY OF SUCH DAMAGES.

% This effect file uses colors
% to illustrate a number of shading vectors -- that is, values
% that are typically important in shading. This effect can often
% help find bogus parts of models, or be used to explore the contents
% of a model.

keywords: material debug virtual_machine bumpmap

date: 070403


keywords: DirectX10
// Note that this version has twin versions of all techniques,
//   so that this single effect file can be used in *either*
//   DirectX9 or DirectX10

To learn more about shading, shaders, and to bounce ideas off other shader
    authors and users, visit the NVIDIA Shader Library Forums at:

    http://developer.nvidia.com/forums/

*******************************************************************************
******************************************************************************/

/*****************************************************************/
/*** HOST APPLICATION IDENTIFIERS ********************************/
/*** Potentially predefined by varying host environments *********/
/*****************************************************************/

// #define _XSI_		/* predefined when running in XSI */
// #define TORQUE		/* predefined in TGEA 1.7 and up */
// #define _3DSMAX_		/* predefined in 3DS Max */
#ifdef _3DSMAX_
int ParamID = 0x0003;		/* Used by Max to select the correct parser */
#endif /* _3DSMAX_ */
#ifdef _XSI_
#define Main Static		/* Technique name used for export to XNA */
#endif /* _XSI_ */

#ifndef FXCOMPOSER_VERSION	/* for very old versions */
#define FXCOMPOSER_VERSION 180
#endif /* FXCOMPOSER_VERSION */

#ifndef DIRECT3D_VERSION
#define DIRECT3D_VERSION 0xb00
#endif /* DIRECT3D_VERSION */

#define FLIP_TEXTURE_Y	/* Different in OpenGL & DirectX */

/*****************************************************************/
/*** EFFECT-SPECIFIC CODE BEGINS HERE ****************************/
/*****************************************************************/
//
// Un-Comment the PROCEDURAL_TEXTURE macro to enable texture generation in
//      DirectX9 ONLY
// DirectX10 may not issue errors, but will generate no texture either
//
// #define PROCEDURAL_TEXTURE
//

//
// Note use of "ungarian Notation" "g" to indicate globally-scaped values
//

/******* Lighting Macros *******/
/** To use "Object-Space" lighting definitions, change these two macros: **/
#define LIGHT_COORDS "World"
// #define OBJECT_SPACE_LIGHTS /* Define if LIGHT_COORDS is "Object" */

#include <include\\debug_tools.fxh>

/**** UNTWEAKABLES: Hidden & Automatically-Tracked Parameters **********/

// transform object vertices to world-space:
float4x4 gWorldXf : World < string UIWidget="None"; >;
// transform object normals, tangents, & binormals to world-space:
float4x4 gWorldITXf : WorldInverseTranspose < string UIWidget="None"; >;
// transform object vertices to view space and project them in perspective:
float4x4 gWvpXf : WorldViewProjection < string UIWidget="None"; >;
// provide tranform from "view" or "eye" coords back to world-space:
float4x4 gViewIXf : ViewInverse < string UIWidget="None"; >;

float2 gScreenSize : VIEWPORTPIXELSIZE < string UIWidget="None"; >;

/************************************************************/
/*** TWEAKABLES *********************************************/
/************************************************************/

float3 gLamp0Pos : POSITION <
    string Object = "PointLight0";
    string UIName =  "Lamp 0 Position";
    string Space = (LIGHT_COORDS);
> = {-0.5f,2.0f,1.25f};

float gScale : UNITSSCALE <
    string units = "inches";
    string UIWidget = "slider";
    float UIMin = 0.001;
    float UIMax = 100.0;
    float UIStep = 0.01;
    string UIName = "Derivatives Brightness";
> = 64.0;

float gShading <
    string UIWidget = "slider";
    float uimin = 0.0;
    float uimax = 1.0;
    float uistep = 0.01;
    string UIName = "Flat<->Shaded";
> = 0.0;

float gNormalGeom <
    string UIWidget = "slider";
    float uimin = 0.0;
    float uimax = 1.0;
    float uistep = 0.01;
    string UIName = "Normals as Geometry";
> = 0.0;

float gUVGeom <
    string UIWidget = "slider";
    float uimin = 0.0;
    float uimax = 1.0;
    float uistep = 0.01;
    string UIName = "UVs as Geometry";
> = 0.0;

float gNGRad <
    string UIWidget = "slider";
    float uimin = 1.0;
    float uimax = 10.0;
    float uistep = 0.01;
    string UIName = "Size of ALternate Geometry";
> = 1.0;

// shared shadow mapping supported in Cg version

/************* DATA STRUCTS **************/

/* data from application vertex buffer */
struct appdata {
    float3 Pos    : POSITION;
    float2 UV        : TEXCOORD0;
    float3 Normal    : NORMAL;
    float3 Tangent    : TANGENT0;
    float3 Binormal    : BINORMAL0;
};

/* data passed from vertex shader to pixel shader */
struct dbgVertOut {
    float4 HPosition    : POSITION;
    float2 TexCoord    : TEXCOORD0;
    float3 LightVec    : TEXCOORD1;
    float3 WorldNormal    : TEXCOORD2;
    float3 WorldEyeVec    : TEXCOORD3;
    float3 WorldTangent    : TEXCOORD4;
    float3 WorldBinorm    : TEXCOORD5;
    float3 WorldPos    : TEXCOORD6;
    float4 BaseColor : COLOR0;
};

/*********** vertex shader for all ******/

dbgVertOut debugVS(appdata IN,
    uniform float4x4 WorldITXf, // our four standard "untweakable" xforms
	uniform float4x4 WorldXf,
	uniform float4x4 ViewIXf,
	uniform float4x4 WvpXf,
    uniform float3 LampPos
) {
    dbgVertOut OUT;
    float4 Po = float4(IN.Pos,1.0);
    float4 normPo = float4((gNGRad*IN.Normal.xyz),1.0);
    Po = lerp(Po,normPo,gNormalGeom);
    float4 uvPo = float4((gNGRad*IN.UV.xy),0.0,1.0);
    Po = lerp(Po,uvPo,gUVGeom);
    OUT.HPosition = mul(Po,WvpXf);
    // OUT.HPosition = mul(WvpXf,Po);
    OUT.WorldNormal = mul(WorldITXf,IN.Normal).xyz;
    OUT.WorldTangent = mul(WorldITXf,IN.Tangent).xyz;
    OUT.WorldBinorm = mul(WorldITXf,IN.Binormal).xyz;
    float4 Pw = mul(WorldXf,Po);
    OUT.LightVec = (LampPos-Pw.xyz);
    OUT.TexCoord = IN.UV.xy;
    OUT.WorldPos = Pw.xyz;
    OUT.WorldEyeVec = normalize(ViewIXf[3].xyz - Pw.xyz);
    float ldn = dot(normalize(OUT.LightVec),normalize(OUT.WorldNormal));
    ldn = max(0,ldn);
    OUT.BaseColor = lerp(float4(1,1,1,1),ldn.xxxx,gShading);
    return OUT;
}

/********* pixel shaders ********/

float4 debug_rgba(dbgVertOut IN,float3 Vec)
{
    float4 vc = as_rgba(Vec);
    float4 InColor = IN.BaseColor;
    return (InColor * vc);
}

float4 debug_rgba_n(dbgVertOut IN,float3 Vec)
{
    float4 vc = as_rgba_n(Vec);
    float4 InColor = IN.BaseColor;
    return (InColor * vc);
}

////////

float4 normalsRawPS(dbgVertOut IN) : COLOR { return debug_rgba(IN,IN.WorldNormal); }
float4 normalsNPS(dbgVertOut IN)   : COLOR { return debug_rgba_n(IN,IN.WorldNormal); }
float4 tangentRawPS(dbgVertOut IN) : COLOR { return debug_rgba(IN,IN.WorldTangent); }
float4 tangentNPS(dbgVertOut IN)   : COLOR { return debug_rgba_n(IN,IN.WorldTangent); }
float4 binormRawPS(dbgVertOut IN)  : COLOR { return debug_rgba(IN,IN.WorldBinorm); }
float4 binormNPS(dbgVertOut IN)    : COLOR { return debug_rgba_n(IN,IN.WorldBinorm); }
float4 viewNPS(dbgVertOut IN)      : COLOR { return debug_rgba(IN,IN.WorldEyeVec); }
float4 lightNPS(dbgVertOut IN)     : COLOR { return debug_rgba_n(IN,IN.LightVec); }

float4 uvcPS(dbgVertOut IN) : COLOR { return debug_rgba(IN,float3(IN.TexCoord.xy,0)); }

float4 vFacePS(dbgVertOut IN,float Vf : VFACE) : COLOR {
    float d = 0;
    if (Vf>0) d = 1;
    return debug_rgba(IN,d.xxx);
}

#if DIRECT3D_VERSION < 0xa00
float4 vPosPS(dbgVertOut IN,float2 Vpos : VPOS) : COLOR {
    float2 c = Vpos.xy / gScreenSize.xy;
    return debug_rgba(IN,float3(c.xy,0));
}
#endif /* DIRECT3D_VERSION < 0xa00 */

float4 uvDerivsPS(dbgVertOut IN) : COLOR
{
    float2 dd = gScale * (abs(ddx(IN.TexCoord)) + abs(ddy(IN.TexCoord)));
    return debug_rgba(IN,float3(dd.xy,0));
}

float4 dPduNPS(dbgVertOut IN) : COLOR
{
    float3 dPx = ddx(IN.TexCoord.x) * ddx(IN.WorldPos);
    float3 dPy = ddy(IN.TexCoord.x) * ddy(IN.WorldPos);
    return debug_rgba(IN,(dPx+dPy));
}

float4 dPdvNPS(dbgVertOut IN) : COLOR
{
    float3 dPx = ddx(IN.TexCoord.y) * ddx(IN.WorldPos);
    float3 dPy = ddy(IN.TexCoord.y) * ddy(IN.WorldPos);
    return debug_rgba_n(IN,(dPx+dPy));
}

float4 halfAnglePS(dbgVertOut IN) :COLOR {
    float3 Ln = normalize(IN.LightVec);
    float3 Vn = normalize(IN.WorldEyeVec);
    // float3 Hn = normalize(Vn + Ln);
    return debug_rgba_n(IN,(Vn+Ln));
}

float4 facingPS(dbgVertOut IN) :COLOR {
    float3 Nn = normalize(IN.WorldNormal);
    float3 Vn = normalize(IN.WorldEyeVec);
    return debug_rgba(IN,float3(abs(dot(Nn,Vn)).xxx));
}

/*
float4 dPduNxPS(dbgVertOut IN) : COLOR
{
    float3 dPx = ddx(IN.TexCoord.x) * ddx(IN.WorldPos);
    float3 dPy = ddy(IN.TexCoord.x) * ddy(IN.WorldPos);
    float3 dPdu = normalize(dPx+dPy);
    float3 Nn = normalize(IN.WorldNormal);
    float3 nTan = cross(dPdu,Nn);
    return debug_rgba(IN,nTan);
}
*/

///////////////////////////////////////
/// TECHNIQUES ////////////////////////
///////////////////////////////////////

#if DIRECT3D_VERSION >= 0xa00
//
// Standard DirectX10 Material State Blocks
//
RasterizerState DisableCulling { CullMode = NONE; };
DepthStencilState DepthEnabling { DepthEnable = TRUE; };
DepthStencilState DepthDisabling {
	DepthEnable = FALSE;
	DepthWriteMask = ZERO;
};
BlendState DisableBlend { BlendEnable[0] = FALSE; };

technique10 uv_Coordinates10 <
	string Script = "Pass=p0;";
> {
    pass p0 <
	string Script = "Draw=geometry;";
    > {
        SetVertexShader( CompileShader( vs_4_0, debugVS(gWorldITXf,gWorldXf,
				gViewIXf,gWvpXf,gLamp0Pos) ) );
        SetGeometryShader( NULL );
        SetPixelShader( CompileShader( ps_4_0, uvcPS() ) );
	    SetRasterizerState(DisableCulling);
	    SetDepthStencilState(DepthEnabling, 0);
	    SetBlendState(DisableBlend, float4( 0.0f, 0.0f, 0.0f, 0.0f ), 0xFFFFFFFF);
    }
}

#endif /* DIRECT3D_VERSION >= 0xa00 */

technique uv_Coordinates <
	string Script = "Pass=p0;";
> {
    pass p0 <
	string Script = "Draw=geometry;";
    > {
        VertexShader = compile vs_3_0 debugVS(gWorldITXf,gWorldXf,
				gViewIXf,gWvpXf,gLamp0Pos);
		ZEnable = true;
		ZWriteEnable = true;
		ZFunc = LessEqual;
		AlphaBlendEnable = false;
		CullMode = None;
        PixelShader = compile ps_3_0 uvcPS();
    }
}

#if DIRECT3D_VERSION >= 0xa00

technique10 worldNormalVecs_Raw10 <
	string Script = "Pass=p0;";
> {
    pass p0 <
	string Script = "Draw=geometry;";
    > {
        SetVertexShader( CompileShader( vs_4_0, debugVS(gWorldITXf,gWorldXf,
				gViewIXf,gWvpXf,gLamp0Pos) ) );
        SetGeometryShader( NULL );
        SetPixelShader( CompileShader( ps_4_0, normalsRawPS() ) );
	    SetRasterizerState(DisableCulling);
	    SetDepthStencilState(DepthEnabling, 0);
	    SetBlendState(DisableBlend, float4( 0.0f, 0.0f, 0.0f, 0.0f ), 0xFFFFFFFF);
    }
}

#endif /* DIRECT3D_VERSION >= 0xa00 */

technique worldNormalVecs_Raw <
	string Script = "Pass=p0;";
> {
    pass p0 <
	string Script = "Draw=geometry;";
    > {
        VertexShader = compile vs_3_0 debugVS(gWorldITXf,gWorldXf,
				gViewIXf,gWvpXf,gLamp0Pos);
		ZEnable = true;
		ZWriteEnable = true;
		ZFunc = LessEqual;
		AlphaBlendEnable = false;
		CullMode = None;
        PixelShader = compile ps_3_0 normalsRawPS();
    }
}

#if DIRECT3D_VERSION >= 0xa00

technique10 worldNormalVecs_Normalized10 <
	string Script = "Pass=p0;";
> {
    pass p0 <
	string Script = "Draw=geometry;";
    > {
        SetVertexShader( CompileShader( vs_4_0, debugVS(gWorldITXf,gWorldXf,
				gViewIXf,gWvpXf,gLamp0Pos) ) );
        SetGeometryShader( NULL );
        SetPixelShader( CompileShader( ps_4_0, normalsNPS() ) );
	    SetRasterizerState(DisableCulling);
	    SetDepthStencilState(DepthEnabling, 0);
	    SetBlendState(DisableBlend, float4( 0.0f, 0.0f, 0.0f, 0.0f ), 0xFFFFFFFF);
    }
}

#endif /* DIRECT3D_VERSION >= 0xa00 */

technique worldNormalVecs_Normalized <
	string Script = "Pass=p0;";
> {
    pass p0 <
	string Script = "Draw=geometry;";
    > {
        VertexShader = compile vs_3_0 debugVS(gWorldITXf,gWorldXf,
				gViewIXf,gWvpXf,gLamp0Pos);
		ZEnable = true;
		ZWriteEnable = true;
		ZFunc = LessEqual;
		AlphaBlendEnable = false;
		CullMode = None;
        PixelShader = compile ps_3_0 normalsNPS();
    }
}

#if DIRECT3D_VERSION >= 0xa00

technique10 worldTangentVecs_Raw10 <
	string Script = "Pass=p0;";
> {
    pass p0 <
	string Script = "Draw=geometry;";
    > {
        SetVertexShader( CompileShader( vs_4_0, debugVS(gWorldITXf,gWorldXf,
				gViewIXf,gWvpXf,gLamp0Pos) ) );
        SetGeometryShader( NULL );
        SetPixelShader( CompileShader( ps_4_0, tangentRawPS() ) );
	    SetRasterizerState(DisableCulling);
	    SetDepthStencilState(DepthEnabling, 0);
	    SetBlendState(DisableBlend, float4( 0.0f, 0.0f, 0.0f, 0.0f ), 0xFFFFFFFF);
    }
}

#endif /* DIRECT3D_VERSION >= 0xa00 */

technique worldTangentVecs_Raw <
	string Script = "Pass=p0;";
> {
    pass p0 <
	string Script = "Draw=geometry;";
    > {
        VertexShader = compile vs_3_0 debugVS(gWorldITXf,gWorldXf,
				gViewIXf,gWvpXf,gLamp0Pos);
		ZEnable = true;
		ZWriteEnable = true;
		ZFunc = LessEqual;
		AlphaBlendEnable = false;
		CullMode = None;
        PixelShader = compile ps_3_0 tangentRawPS();
    }
}

#if DIRECT3D_VERSION >= 0xa00

technique10 worldTangentVecs_Normalized10 <
	string Script = "Pass=p0;";
> {
    pass p0 <
	string Script = "Draw=geometry;";
    > {
        SetVertexShader( CompileShader( vs_4_0, debugVS(gWorldITXf,gWorldXf,
				gViewIXf,gWvpXf,gLamp0Pos) ) );
        SetGeometryShader( NULL );
        SetPixelShader( CompileShader( ps_4_0, tangentNPS() ) );
	    SetRasterizerState(DisableCulling);
	    SetDepthStencilState(DepthEnabling, 0);
	    SetBlendState(DisableBlend, float4( 0.0f, 0.0f, 0.0f, 0.0f ), 0xFFFFFFFF);
    }
}

#endif /* DIRECT3D_VERSION >= 0xa00 */

technique worldTangentVecs_Normalized <
	string Script = "Pass=p0;";
> {
    pass p0 <
	string Script = "Draw=geometry;";
    > {
        VertexShader = compile vs_3_0 debugVS(gWorldITXf,gWorldXf,
				gViewIXf,gWvpXf,gLamp0Pos);
		ZEnable = true;
		ZWriteEnable = true;
		ZFunc = LessEqual;
		AlphaBlendEnable = false;
		CullMode = None;
        PixelShader = compile ps_3_0 tangentNPS();
    }
}

#if DIRECT3D_VERSION >= 0xa00

technique10 worldBinormalVecs_Raw10 <
	string Script = "Pass=p0;";
> {
    pass p0 <
	string Script = "Draw=geometry;";
    > {
        SetVertexShader( CompileShader( vs_4_0, debugVS(gWorldITXf,gWorldXf,
				gViewIXf,gWvpXf,gLamp0Pos) ) );
        SetGeometryShader( NULL );
        SetPixelShader( CompileShader( ps_4_0, binormRawPS() ) );
	    SetRasterizerState(DisableCulling);
	    SetDepthStencilState(DepthEnabling, 0);
	    SetBlendState(DisableBlend, float4( 0.0f, 0.0f, 0.0f, 0.0f ), 0xFFFFFFFF);
    }
}

#endif /* DIRECT3D_VERSION >= 0xa00 */

technique worldBinormalVecs_Raw <
	string Script = "Pass=p0;";
> {
    pass p0 <
	string Script = "Draw=geometry;";
    > {
        VertexShader = compile vs_3_0 debugVS(gWorldITXf,gWorldXf,
				gViewIXf,gWvpXf,gLamp0Pos);
		ZEnable = true;
		ZWriteEnable = true;
		ZFunc = LessEqual;
		AlphaBlendEnable = false;
		CullMode = None;
        PixelShader = compile ps_3_0 binormRawPS();
    }
}

#if DIRECT3D_VERSION >= 0xa00

technique10 worldBinormalVecs_Normalized10 <
	string Script = "Pass=p0;";
> {
    pass p0 <
	string Script = "Draw=geometry;";
    > {
        SetVertexShader( CompileShader( vs_4_0, debugVS(gWorldITXf,gWorldXf,
				gViewIXf,gWvpXf,gLamp0Pos) ) );
        SetGeometryShader( NULL );
        SetPixelShader( CompileShader( ps_4_0, binormNPS() ) );
	    SetRasterizerState(DisableCulling);
	    SetDepthStencilState(DepthEnabling, 0);
	    SetBlendState(DisableBlend, float4( 0.0f, 0.0f, 0.0f, 0.0f ), 0xFFFFFFFF);
    }
}

#endif /* DIRECT3D_VERSION >= 0xa00 */

technique worldBinormalVecs_Normalized <
	string Script = "Pass=p0;";
> {
    pass p0 <
	string Script = "Draw=geometry;";
    > {
        VertexShader = compile vs_3_0 debugVS(gWorldITXf,gWorldXf,
				gViewIXf,gWvpXf,gLamp0Pos);
		ZEnable = true;
		ZWriteEnable = true;
		ZFunc = LessEqual;
		AlphaBlendEnable = false;
		CullMode = None;
        PixelShader = compile ps_3_0 binormNPS();
    }
}

#if DIRECT3D_VERSION >= 0xa00

technique10 worldViewVec_Normalized10 <
	string Script = "Pass=p0;";
> {
    pass p0 <
	string Script = "Draw=geometry;";
    > {
        SetVertexShader( CompileShader( vs_4_0, debugVS(gWorldITXf,gWorldXf,
				gViewIXf,gWvpXf,gLamp0Pos) ) );
        SetGeometryShader( NULL );
        SetPixelShader( CompileShader( ps_4_0, viewNPS() ) );
	    SetRasterizerState(DisableCulling);
	    SetDepthStencilState(DepthEnabling, 0);
	    SetBlendState(DisableBlend, float4( 0.0f, 0.0f, 0.0f, 0.0f ), 0xFFFFFFFF);
    }
}

#endif /* DIRECT3D_VERSION >= 0xa00 */

technique worldViewVec_Normalized <
	string Script = "Pass=p0;";
> {
    pass p0 <
	string Script = "Draw=geometry;";
    > {
        VertexShader = compile vs_3_0 debugVS(gWorldITXf,gWorldXf,
				gViewIXf,gWvpXf,gLamp0Pos);
		ZEnable = true;
		ZWriteEnable = true;
		ZFunc = LessEqual;
		AlphaBlendEnable = false;
		CullMode = None;
        PixelShader = compile ps_3_0 viewNPS();
    }
}

#if DIRECT3D_VERSION >= 0xa00

technique10 worldLightVec_Normalized10 <
	string Script = "Pass=p0;";
> {
    pass p0 <
	string Script = "Draw=geometry;";
    > {
        SetVertexShader( CompileShader( vs_4_0, debugVS(gWorldITXf,gWorldXf,
				gViewIXf,gWvpXf,gLamp0Pos) ) );
        SetGeometryShader( NULL );
        SetPixelShader( CompileShader( ps_4_0, lightNPS() ) );
	    SetRasterizerState(DisableCulling);
	    SetDepthStencilState(DepthEnabling, 0);
	    SetBlendState(DisableBlend, float4( 0.0f, 0.0f, 0.0f, 0.0f ), 0xFFFFFFFF);
    }
}

#endif /* DIRECT3D_VERSION >= 0xa00 */

technique worldLightVec_Normalized <
	string Script = "Pass=p0;";
> {
    pass p0 <
	string Script = "Draw=geometry;";
    > {
        VertexShader = compile vs_3_0 debugVS(gWorldITXf,gWorldXf,
				gViewIXf,gWvpXf,gLamp0Pos);
		ZEnable = true;
		ZWriteEnable = true;
		ZFunc = LessEqual;
		AlphaBlendEnable = false;
		CullMode = None;
        PixelShader = compile ps_3_0 lightNPS();
    }
}

#if DIRECT3D_VERSION >= 0xa00

technique10 halfAngles10 <
	string Script = "Pass=p0;";
> {
    pass p0 <
	string Script = "Draw=geometry;";
    > {
        SetVertexShader( CompileShader( vs_4_0, debugVS(gWorldITXf,gWorldXf,
				gViewIXf,gWvpXf,gLamp0Pos) ) );
        SetGeometryShader( NULL );
        SetPixelShader( CompileShader( ps_4_0, halfAnglePS() ) );
	    SetRasterizerState(DisableCulling);
	    SetDepthStencilState(DepthEnabling, 0);
	    SetBlendState(DisableBlend, float4( 0.0f, 0.0f, 0.0f, 0.0f ), 0xFFFFFFFF);
    }
}

#endif /* DIRECT3D_VERSION >= 0xa00 */

technique halfAngles <
	string Script = "Pass=p0;";
> {
    pass p0 <
	string Script = "Draw=geometry;";
    > {
        VertexShader = compile vs_3_0 debugVS(gWorldITXf,gWorldXf,
				gViewIXf,gWvpXf,gLamp0Pos);
		ZEnable = true;
		ZWriteEnable = true;
		ZFunc = LessEqual;
		AlphaBlendEnable = false;
		CullMode = None;
        PixelShader = compile ps_3_0 halfAnglePS();
    }
}

#if DIRECT3D_VERSION >= 0xa00

technique10 facingRatio10 <
	string Script = "Pass=p0;";
> {
    pass p0 <
	string Script = "Draw=geometry;";
    > {
        SetVertexShader( CompileShader( vs_4_0, debugVS(gWorldITXf,gWorldXf,
				gViewIXf,gWvpXf,gLamp0Pos) ) );
        SetGeometryShader( NULL );
        SetPixelShader( CompileShader( ps_4_0, facingPS() ) );
	    SetRasterizerState(DisableCulling);
	    SetDepthStencilState(DepthEnabling, 0);
	    SetBlendState(DisableBlend, float4( 0.0f, 0.0f, 0.0f, 0.0f ), 0xFFFFFFFF);
    }
}

#endif /* DIRECT3D_VERSION >= 0xa00 */

technique facingRatio <
	string Script = "Pass=p0;";
> {
    pass p0 <
	string Script = "Draw=geometry;";
    > {
        VertexShader = compile vs_3_0 debugVS(gWorldITXf,gWorldXf,
				gViewIXf,gWvpXf,gLamp0Pos);
		ZEnable = true;
		ZWriteEnable = true;
		ZFunc = LessEqual;
		AlphaBlendEnable = false;
		CullMode = None;
        PixelShader = compile ps_3_0 facingPS();
    }
}

#if DIRECT3D_VERSION >= 0xa00

technique10 uv_Derivatives10 <
	string Script = "Pass=p0;";
> {
    pass p0 <
	string Script = "Draw=geometry;";
    > {
        SetVertexShader( CompileShader( vs_4_0, debugVS(gWorldITXf,gWorldXf,
				gViewIXf,gWvpXf,gLamp0Pos) ) );
        SetGeometryShader( NULL );
        SetPixelShader( CompileShader( ps_4_0, uvDerivsPS() ) );
	    SetRasterizerState(DisableCulling);
	    SetDepthStencilState(DepthEnabling, 0);
	    SetBlendState(DisableBlend, float4( 0.0f, 0.0f, 0.0f, 0.0f ), 0xFFFFFFFF);
    }
}

#endif /* DIRECT3D_VERSION >= 0xa00 */

technique uv_Derivatives <
	string Script = "Pass=p0;";
> {
    pass p0 <
	string Script = "Draw=geometry;";
    > {
        VertexShader = compile vs_3_0 debugVS(gWorldITXf,gWorldXf,
				gViewIXf,gWvpXf,gLamp0Pos);
		ZEnable = true;
		ZWriteEnable = true;
		ZFunc = LessEqual;
		AlphaBlendEnable = false;
		CullMode = None;
        PixelShader = compile ps_3_0 uvDerivsPS();
    }
}

#if DIRECT3D_VERSION >= 0xa00

technique10 dPdu_Normalized10 <
	string Script = "Pass=p0;";
> {
    pass p0 <
	string Script = "Draw=geometry;";
    > {
        SetVertexShader( CompileShader( vs_4_0, debugVS(gWorldITXf,gWorldXf,
				gViewIXf,gWvpXf,gLamp0Pos) ) );
        SetGeometryShader( NULL );
        SetPixelShader( CompileShader( ps_4_0, dPduNPS() ) );
	    SetRasterizerState(DisableCulling);
	    SetDepthStencilState(DepthEnabling, 0);
	    SetBlendState(DisableBlend, float4( 0.0f, 0.0f, 0.0f, 0.0f ), 0xFFFFFFFF);
    }
}

#endif /* DIRECT3D_VERSION >= 0xa00 */

technique dPdu_Normalized <
	string Script = "Pass=p0;";
> {
    pass p0 <
	string Script = "Draw=geometry;";
    > {
        VertexShader = compile vs_3_0 debugVS(gWorldITXf,gWorldXf,
				gViewIXf,gWvpXf,gLamp0Pos);
		ZEnable = true;
		ZWriteEnable = true;
		ZFunc = LessEqual;
		AlphaBlendEnable = false;
		CullMode = None;
        PixelShader = compile ps_3_0 dPduNPS();
    }
}

#if DIRECT3D_VERSION >= 0xa00

technique10 dPdv_Normalized10 <
	string Script = "Pass=p0;";
> {
    pass p0 <
	string Script = "Draw=geometry;";
    > {
        SetVertexShader( CompileShader( vs_4_0, debugVS(gWorldITXf,gWorldXf,
				gViewIXf,gWvpXf,gLamp0Pos) ) );
        SetGeometryShader( NULL );
        SetPixelShader( CompileShader( ps_4_0, dPdvNPS() ) );
	    SetRasterizerState(DisableCulling);
	    SetDepthStencilState(DepthEnabling, 0);
	    SetBlendState(DisableBlend, float4( 0.0f, 0.0f, 0.0f, 0.0f ), 0xFFFFFFFF);
    }
}

#endif /* DIRECT3D_VERSION >= 0xa00 */

technique dPdv_Normalized <
	string Script = "Pass=p0;";
> {
    pass p0 <
	string Script = "Draw=geometry;";
    > {
        VertexShader = compile vs_3_0 debugVS(gWorldITXf,gWorldXf,
				gViewIXf,gWvpXf,gLamp0Pos);
		ZEnable = true;
		ZWriteEnable = true;
		ZFunc = LessEqual;
		AlphaBlendEnable = false;
		CullMode = None;
        PixelShader = compile ps_3_0 dPdvNPS();
    }
}

#if DIRECT3D_VERSION >= 0xa00

technique10 vFace_Register10 <
	string Script = "Pass=p0;";
> {
    pass p0 <
	string Script = "Draw=geometry;";
    > {
        SetVertexShader( CompileShader( vs_4_0, debugVS(gWorldITXf,gWorldXf,
				gViewIXf,gWvpXf,gLamp0Pos) ) );
        SetGeometryShader( NULL );
        SetPixelShader( CompileShader( ps_4_0, vFacePS() ) );
	    SetRasterizerState(DisableCulling);
	    SetDepthStencilState(DepthEnabling, 0);
	    SetBlendState(DisableBlend, float4( 0.0f, 0.0f, 0.0f, 0.0f ), 0xFFFFFFFF);
    }
}

#endif /* DIRECT3D_VERSION >= 0xa00 */

technique vFace_Register <
	string Script = "Pass=p0;";
> {
    pass p0 <
	string Script = "Draw=geometry;";
    > {
        VertexShader = compile vs_3_0 debugVS(gWorldITXf,gWorldXf,
				gViewIXf,gWvpXf,gLamp0Pos);
		ZEnable = true;
		ZWriteEnable = true;
		ZFunc = LessEqual;
		AlphaBlendEnable = false;
		CullMode = None;
        PixelShader = compile ps_3_0 vFacePS();
    }
}

#if DIRECT3D_VERSION < 0xa00
technique vPos_Register <
	string Script = "Pass=p0;";
> {
    pass p0 <
	string Script = "Draw=geometry;";
    > {
        VertexShader = compile vs_3_0 debugVS(gWorldITXf,gWorldXf,
				gViewIXf,gWvpXf,gLamp0Pos);
		ZEnable = true;
		ZWriteEnable = true;
		ZFunc = LessEqual;
		AlphaBlendEnable = false;
		CullMode = None;
        PixelShader = compile ps_3_0 vPosPS();
    }
}

#endif /* DIRECT3D_VERSION < 0xa00 */
// # debug_tech(dPduX,debugVS,dPduNxPS)

/***************************** eof ***/
