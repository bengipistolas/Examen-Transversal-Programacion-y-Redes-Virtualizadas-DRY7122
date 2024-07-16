def verificar_rango_vlan(vlan_id):
    if 1 <= vlan_id <= 1005:
        return "VLAN en rango normal"
    elif 1006 <= vlan_id <= 4094:
        return "VLAN en rango extendido"
    else:
        return "VLAN fuera de rango válido"

vlan_id = int(input("Ingrese el número de VLAN: "))
resultado = verificar_rango_vlan(vlan_id)

print(resultado)

