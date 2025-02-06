def generate_intro_html(
    presented_to_name: str,
    presented_to_linkedin: str | None,
    presented_to_company: str,
    presented_name: str,
    presented_linkedin: str | None,
    presented_company: str,
    sender_name: str,
    sender_email: str
) -> str:
    """
    // ... existing code ...
    """
    
    # Função auxiliar para criar o nome com ou sem link
    def create_name_element(name: str, linkedin: str | None) -> str:
        if linkedin:
            return f'<a href="{linkedin}" style="text-decoration: none;" title="Ver perfil no LinkedIn">{name}</a>'
        return name

    # Criar elementos com ou sem link
    presented_to_element = create_name_element(presented_to_name, presented_to_linkedin)
    presented_element = create_name_element(presented_name, presented_linkedin)

    template = f"""
    <div>
        <div dir="ltr">
            <div>
                <div>
                    <div>Fala {presented_to_name}, tudo bem?</div>
                    <div>
                        <p style="margin:0px;padding:0px"><br></p>
                        <p style="margin:0px;padding:0px">Como comentei com você, gostaria de te apresentar o {presented_element}, da {presented_company}.</p>
                        <p style="margin:0px;padding:0px"><br></p>
                        <p style="margin:0px;padding:0px">{presented_name}, te apresento o {presented_to_element}, da {presented_to_company}, fundo mega parceiro nosso.</p>
                        <p style="margin:0px;padding:0px"><br></p>
                        <p style="margin:0px;padding:0px">Vocês já tem o contexto da intro, então bola com vocês para marcarem uma conversa.</p>
                        <p style="margin:0px;padding:0px"><br></p>
                        <p style="margin:0px;padding:0px">Abraço,</p>
                        <p style="margin:0px;padding:0px">{sender_name}</p>
                    </div>

                    <br/>
                    <br/>

                    <table style="color:rgb(80,0,80);border:none;border-collapse:collapse">
                        <colgroup>
                            <col width="110">
                            <col width="514">
                        </colgroup>
                        <tbody>
                            <tr style="height:72.8628pt">
                                <td style="border-right:1.5pt solid rgb(243,208,62);vertical-align:top;padding:5pt;overflow:hidden">
                                    <p dir="ltr" style="line-height:1.38;margin-top:0pt;margin-bottom:0pt">
                                        <span style="font-size:12pt;font-family:Arial;color:rgb(243,208,62);background-color:transparent;font-weight:700;vertical-align:baseline">
                                            <span style="border:none;display:inline-block;overflow:hidden;width:96px;height:96px">
                                                <img src="https://lh3.googleusercontent.com/ohZhe1m9XR3qu_sIUw5cT489Cp7bmXX19XVC_cWabrwshoSvKPHNaq-0B0GgFPTXhUITaHSBODiVsZ4gLzn1ifp5u2QfnDFTUcUwubvW7CQ9YZ03hAHy3H-MaVO_kNwQ530-4feLkYo1Erw4GZTwFbE"
                                                    width="96" height="96" style="margin-left:0px;margin-top:0px" crossorigin="">
                                            </span>
                                        </span>
                                    </p>
                                </td>
                                <td style="border-left:1.5pt solid rgb(243,208,62);vertical-align:top;padding:5pt;overflow:hidden">
                                    <p dir="ltr" style="line-height:1.2;margin-top:0pt;margin-bottom:0pt">
                                        <span style="font-size:12pt;font-family:Courier New;color:rgb(33,33,33);background-color:transparent;font-weight:700;vertical-align:baseline">{sender_name}</span>
                                    </p>
                                    <p dir="ltr" style="line-height:1.2;margin-top:0pt;margin-bottom:0pt">
                                        <span style="font-size:7pt;font-family:Gill Sans,sans-serif;color:rgb(67,67,67);background-color:transparent;vertical-align:baseline">{sender_email}</span>
                                    </p>
                                    <p dir="ltr" style="line-height:1.2;margin-top:0pt;margin-bottom:0pt">
                                        <span style="font-size:7pt;font-family:Gill Sans,sans-serif;color:rgb(127,127,127);background-color:transparent;vertical-align:baseline">Rua dos Pinheiros 623 | 5th floor</span>
                                    </p>
                                    <p dir="ltr" style="line-height:1.2;margin-top:0pt;margin-bottom:0pt">
                                        <span style="font-size:7pt;font-family:Gill Sans,sans-serif;color:rgb(127,127,127);background-color:transparent;vertical-align:baseline">Pinheiros, São Paulo</span>
                                    </p>
                                    <p dir="ltr" style="line-height:1.2;margin-top:0pt;margin-bottom:0pt">
                                        <span style="font-size:7pt;font-family:Gill Sans,sans-serif;color:rgb(127,127,127);background-color:transparent;vertical-align:baseline">norte.ventures</span>
                                    </p>
                                </td>
                            </tr>
                        </tbody>
                    </table>
                </div>
            </div>
        </div>
    </div>
    """
    return template