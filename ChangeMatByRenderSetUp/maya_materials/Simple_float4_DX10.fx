//**************************************************************************/
// Copyright (c) 2012 Autodesk, Inc.
// All rights reserved.
// 
// These coded instructions, statements, and computer programs contain
// unpublished proprietary information written by Autodesk, Inc., and are
// protected by Federal copyright law. They may not be disclosed to third
// parties or copied or duplicated in any form, in whole or in part, without
// the prior written consent of Autodesk, Inc.
//**************************************************************************/

// World-view-projection transformation.
float4x4 gWVPXf : WorldViewProjection < string UIWidget = "None"; >;

// Vertex shader input structure.
struct VS_INPUT
{
    float4 Pos : POSITION;
    float4 Norm : NORMAL;
	float4 Tang : TANGENT;
	float4 Binorm : BINORMAL;
};

// Vertex shader output structure.
struct VS_TO_PS
{
    float4 HPos : SV_Position;
    float4 Norm : NORMAL;
	float4 Tang : TANGENT;
	float4 Binorm : BINORMAL;
};

// Vertex shader.
VS_TO_PS VS(VS_INPUT In)
{
    VS_TO_PS Out;

    // Transform the position from world space to clip space for output.
    Out.HPos = mul(In.Pos, gWVPXf);

    Out.Norm = In.Norm;
	Out.Tang = In.Tang;
	Out.Binorm = In.Binorm;

    return Out;
}

// Pixel shader.
float4 PS0(VS_TO_PS In) : SV_Target
{
    return In.Norm;
}

float4 PS1(VS_TO_PS In) : SV_Target
{
    return In.Tang;
}

float4 PS2(VS_TO_PS In) : SV_Target
{
    return In.Binorm;
}

// Techniques.
technique11 Normal4AsColor
{
    pass P0
    {
        SetVertexShader(CompileShader(vs_5_0, VS()));
        SetGeometryShader(NULL);
        SetPixelShader(CompileShader(ps_5_0, PS0()));
    }
}

technique11 Tangent4AsColor
{
    pass P0
    {
        SetVertexShader(CompileShader(vs_5_0, VS()));
        SetGeometryShader(NULL);
        SetPixelShader(CompileShader(ps_5_0, PS1()));
    }
}

technique11 Binormal4AsColor
{
    pass P0
    {
        SetVertexShader(CompileShader(vs_5_0, VS()));
        SetGeometryShader(NULL);
        SetPixelShader(CompileShader(ps_5_0, PS2()));
    }
}
