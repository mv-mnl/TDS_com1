import math

def imprimir_resultados(res):
    print("\n" + "="*50)
    print("                 RESULTADOS")
    print("="*50)
    for clave, valor in res.items():
        if isinstance(valor, float):
            # Formato moneda si la clave contiene la palabra "Costo"
            if "Costo" in clave:
                print(f"{clave:<35}: ${valor:.2f}")
            else:
                print(f"{clave:<35}: {valor:.4f}")
        else:
            print(f"{clave:<35}: {valor}")
    print("="*50 + "\n")

def calcular_costos(res_dict, s, L):
    """Calcula y añade los costos al diccionario de resultados"""
    print("\n--- ANÁLISIS DE COSTOS ---")
    calcular = input("¿Deseas calcular los costos totales del sistema? (s/n): ").lower()
    
    if calcular == 's':
        try:
            Ce = float(input("Ingresa el Costo por Servidor (Ce) por hora: $"))
            Cq = float(input("Ingresa el Costo de Espera (Cq) por cliente por hora: $"))
            
            costo_servicio = s * Ce
            costo_espera = L * Cq
            costo_total = costo_servicio + costo_espera
            
            res_dict["--- ANÁLISIS ECONÓMICO ---"] = "----------------"
            res_dict["Costo Total del Servicio (S x Ce)"] = costo_servicio
            res_dict["Costo Total de Espera (L x Cq)"] = costo_espera
            res_dict["COSTO TOTAL DEL SISTEMA (Ct)"] = costo_total
            
        except ValueError:
            print("[!] Error en los datos de costo. Se omitirá el cálculo económico.")
    
    return res_dict

def modelo_mm1(lam, mu):
    rho = lam / mu
    if rho >= 1:
        return {"Error": "Sistema inestable (rho >= 1). La cola crecerá infinitamente."}
    
    p0 = 1 - rho
    L = lam / (mu - lam)
    Lq = L - rho
    W = L / lam
    Wq = Lq / lam
    
    res = {"Utilización (rho)": rho, "Prob. Vacío (P0)": p0, 
           "Clientes en sistema (L)": L, "Clientes en cola (Lq)": Lq,
           "Tiempo en sistema (W)": W, "Tiempo en cola (Wq)": Wq}
    return calcular_costos(res, s=1, L=L)

def modelo_mms(lam, mu, s):
    rho = lam / (s * mu)
    if rho >= 1:
        return {"Error": "Sistema inestable (rho >= 1). Necesitas más servidores."}
    
    suma = sum(((lam/mu)**n) / math.factorial(n) for n in range(s))
    termino_s = ((lam/mu)**s) / (math.factorial(s) * (1 - rho))
    p0 = 1 / (suma + termino_s)
    
    Lq = (p0 * ((lam/mu)**s) * rho) / (math.factorial(s) * (1 - rho)**2)
    Wq = Lq / lam
    W = Wq + (1 / mu)
    L = lam * W
    
    res = {"Utilización (rho)": rho, "Prob. Vacío (P0)": p0, 
           "Clientes en sistema (L)": L, "Clientes en cola (Lq)": Lq,
           "Tiempo en sistema (W)": W, "Tiempo en cola (Wq)": Wq}
    return calcular_costos(res, s=s, L=L)

def modelo_mg1(lam, mu, var):
    rho = lam / mu
    if rho >= 1:
        return {"Error": "Sistema inestable (rho >= 1)."}
    
    Lq = ((lam**2) * var + rho**2) / (2 * (1 - rho))
    Wq = Lq / lam
    W = Wq + (1 / mu)
    L = lam * W
    p0 = 1 - rho
    
    res = {"Utilización (rho)": rho, "Prob. Vacío (P0)": p0, 
           "Clientes en sistema (L)": L, "Clientes en cola (Lq)": Lq,
           "Tiempo en sistema (W)": W, "Tiempo en cola (Wq)": Wq}
    return calcular_costos(res, s=1, L=L)

def modelo_mm1k(lam, mu, k):
    rho = lam / mu
    
    if rho == 1:
        p0 = 1 / (k + 1)
        pk = p0
        L = k / 2
    else:
        p0 = (1 - rho) / (1 - rho**(k + 1))
        pk = p0 * (rho**k)
        L = rho * (1 - (k + 1)*rho**k + k*rho**(k + 1)) / ((1 - rho) * (1 - rho**(k + 1)))
        
    lam_eff = lam * (1 - pk)
    Lq = L - (1 - p0)
    W = L / lam_eff
    Wq = Lq / lam_eff
    
    res = {"Utilización Nominal (rho)": rho, "Prob. Bloqueo/Pérdida (Pk)": pk,
           "Tasa Efectiva Llegada (Lam_eff)": lam_eff, "Prob. Vacío (P0)": p0,
           "Clientes en sistema (L)": L, "Clientes en cola (Lq)": Lq,
           "Tiempo en sistema (W)": W, "Tiempo en cola (Wq)": Wq}
    return calcular_costos(res, s=1, L=L)

def modelo_prioridades(lam1, lam2, mu):
    rho1 = lam1 / mu
    rho2 = lam2 / mu
    rho_total = rho1 + rho2
    
    if rho_total >= 1:
        return {"Error": "Sistema inestable. Las tasas de llegada superan la de servicio."}
    
    Wq1 = (rho_total / mu) / (1 - rho1)
    Wq2 = (rho_total / mu) / ((1 - rho1) * (1 - rho_total))
    W1 = Wq1 + (1 / mu)
    W2 = Wq2 + (1 / mu)
    Lq1 = lam1 * Wq1
    Lq2 = lam2 * Wq2
    
    # L total es la suma de los L de ambas prioridades
    L_total = (lam1 * W1) + (lam2 * W2)
    
    res = {"Utilización Total (rho)": rho_total,
           "Tiempo en cola CRÍTICOS (Wq1)": Wq1, "Tiempo en sistema CRÍTICOS (W1)": W1,
           "Tiempo en cola NORMALES (Wq2)": Wq2, "Tiempo en sistema NORMALES (W2)": W2,
           "Clientes en cola CRÍTICOS (Lq1)": Lq1, "Clientes en cola NORMALES (Lq2)": Lq2}
    
    return calcular_costos(res, s=1, L=L_total)

def main():
    while True:
        print("\n=== HERRAMIENTA UNIVERSAL DE TEORÍA DE COLAS ===")
        print("1. Modelo M/M/1 (Un servidor estándar)")
        print("2. Modelo M/M/s (Múltiples servidores)")
        print("3. Modelo M/G/1 (Tiempos variables / Pollaczek-Khinchine)")
        print("4. Modelo M/M/1/K (Capacidad finita / límite de sistema)")
        print("5. Modelo con Prioridades (No-preemptivo, 2 clases)")
        print("6. Salir")
        
        opcion = input("Selecciona el tipo de problema a resolver (1-6): ")
        
        if opcion == '6':
            print("Saliendo de la herramienta...")
            break
            
        try:
            if opcion in ['1', '2', '3', '4']:
                lam = float(input("Ingresa la Tasa de Llegada (Lambda): "))
                mu = float(input("Ingresa la Tasa de Servicio (Mu): "))
                
                if opcion == '1':
                    res = modelo_mm1(lam, mu)
                elif opcion == '2':
                    s = int(input("Ingresa el número de servidores (s): "))
                    res = modelo_mms(lam, mu, s)
                elif opcion == '3':
                    var = float(input("Ingresa la Varianza del tiempo de servicio (misma unidad de tiempo al cuadrado): "))
                    res = modelo_mg1(lam, mu, var)
                elif opcion == '4':
                    k = int(input("Ingresa la Capacidad Máxima del sistema (K): "))
                    res = modelo_mm1k(lam, mu, k)
                    
            elif opcion == '5':
                lam1 = float(input("Ingresa Tasa de Llegada CRÍTICOS (Lambda 1): "))
                lam2 = float(input("Ingresa Tasa de Llegada NORMALES (Lambda 2): "))
                mu = float(input("Ingresa la Tasa de Servicio compartida (Mu): "))
                res = modelo_prioridades(lam1, lam2, mu)
            else:
                print("\n[!] Opción inválida.\n")
                continue
            
            if "Error" in res:
                print(f"\n[!] {res['Error']}\n")
            else:
                imprimir_resultados(res)
            
        except ValueError:
            print("\n[!] Error: Ingresa un número válido. Usa puntos para decimales.\n")

if __name__ == "__main__":
    main()