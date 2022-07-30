float4x4 gWVPXf : WorldViewProjection;

struct VS_INPUT
{
    float4 Pos : POSITION;
};

struct VS_TO_PS
{
    float4 HPos : SV_Position;
};

struct VS_TO_PS_frag
{
    float vFace : VFACE;
};

VS_TO_PS VS(VS_INPUT In)
{
    VS_TO_PS Out;
    Out.HPos = mul(In.Pos, gWVPXf);
    return Out;
}

float4 PS(VS_TO_PS_frag In) : SV_Target
{
    return (In.vFace > 0 ) ? float4(0.0, 0.0, 0.0, 1.0) : float4(1.0, 0.0, 0.0, 1.0);
}

technique11 HelloShader
{
    pass P0
    {
        SetVertexShader(CompileShader(vs_5_0, VS()));
        SetPixelShader(CompileShader(ps_5_0, PS()));
    }
}