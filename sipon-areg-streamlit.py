import streamlit as st
from datetime import datetime, timedelta

def validar_formato_hora(hora_str):
    """Valida se a string está no formato HH:MM correto"""
    try:
        datetime.strptime(hora_str, "%H:%M")
        return True
    except ValueError:
        return False

def calcular_saida(entrada_str, intervalo_inicio_str, intervalo_fim_str):
    """Calcula o horário de saída baseado nos parâmetros fornecidos"""
    try:
        # Converter texto para datetime
        base_data = datetime.today().replace(hour=0, minute=0, second=0, microsecond=0)
        
        hora_entrada = datetime.strptime(entrada_str, "%H:%M").replace(
            year=base_data.year, month=base_data.month, day=base_data.day
        )
        intervalo_inicio = datetime.strptime(intervalo_inicio_str, "%H:%M").replace(
            year=base_data.year, month=base_data.month, day=base_data.day
        )
        intervalo_fim = datetime.strptime(intervalo_fim_str, "%H:%M").replace(
            year=base_data.year, month=base_data.month, day=base_data.day
        )
        
        # Verificações básicas de ordem dos horários
        if not (hora_entrada < intervalo_inicio < intervalo_fim):
            return None, "Horários em ordem incorreta. Verifique os valores digitados."
        
        # Jornada total de 6h
        jornada_total = timedelta(hours=6)
        
        # Cálculo duração intervalo
        duracao_intervalo = intervalo_fim - intervalo_inicio
        
        # 15 minutos do intervalo computados na jornada
        intervalo_extra = duracao_intervalo - timedelta(minutes=15)
        
        # Cálculo do horário de saída
        hora_saida = hora_entrada + jornada_total + intervalo_extra
        
        return hora_saida.strftime('%H:%M'), None
        
    except ValueError as e:
        return None, "Erro no formato dos horários. Use o formato HH:MM (ex: 08:30)."

def main():
    st.set_page_config(
        page_title="Calculadora AREG",
        page_icon="🕐",
        layout="centered"
    )
    
    st.title("🕐 Calculadora AREG - Jornada 6h")
    st.markdown("---")
    
    # Campos de entrada
    st.subheader("Informações do Horário")
    
    col1, col2 = st.columns(2)
    
    with col1:
        entrada = st.text_input(
            "Hora de entrada",
            placeholder="08:00",
            help="Digite no formato HH:MM"
        )
    
    with col2:
        st.write("")  # Espaço em branco para alinhamento
    
    col3, col4 = st.columns(2)
    
    with col3:
        intervalo_inicio = st.text_input(
            "Início do intervalo",
            placeholder="12:00",
            help="Digite no formato HH:MM"
        )
    
    with col4:
        intervalo_fim = st.text_input(
            "Fim do intervalo",
            placeholder="12:30",
            help="Digite no formato HH:MM"
        )
    
    # Botão de cálculo
    st.markdown("---")
    calcular = st.button("🔍 Calcular Horário de Saída", type="secondary")
    
    # Validação e cálculo
    if calcular:
        # Verificar se todos os campos foram preenchidos
        if not entrada or not intervalo_inicio or not intervalo_fim:
            st.error("⚠️ Preencha todos os campos!")
            return
           
        # Formatar automaticamente entradas como '0800' → '08:00'
        if len(entrada) == 4 and entrada.isdigit():
            entrada = entrada[:2] + ":" + entrada[2:]
        if len(intervalo_inicio) == 4 and intervalo_inicio.isdigit():
            intervalo_inicio = intervalo_inicio[:2] + ":" + intervalo_inicio[2:]
        if len(intervalo_fim) == 4 and intervalo_fim.isdigit():
            intervalo_fim = intervalo_fim[:2] + ":" + intervalo_fim[2:]
        
        # Calcular horário de saída
        hora_saida, erro = calcular_saida(entrada, intervalo_inicio, intervalo_fim)
        
        if erro:
            st.error(f"⚠️ {erro}")
        else:
            st.markdown(
    f"""
    <div style='background-color: #d4edda; padding: 15px; border-radius: 8px;'>
        <span style='font-size: 26px; color: #155724;'>🎯 <strong>Horário de saída:</strong> {hora_saida}</span>
    </div>
    """,
    unsafe_allow_html=True
)
        
    # Rodapé
    st.markdown("---")
    st.markdown(
        "<div style='text-align: center; color: gray; font-size: 18px;'>"
        "CAIXA • Desenvolvido por c150930"
        "</div>",
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main()
