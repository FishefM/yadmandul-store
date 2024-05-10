-- drop trigger if exists validar_correo_cliente;

delimiter //
create trigger validar_correo_cliente before insert on clientes
for each row
begin
    declare num_correos int;
    select count(*) into num_correos from clientes where correo_cli = new.correo_cli;
    if num_correos > 0 then
        signal sqlstate '45000'
        set message_text = 'El correo electrónico ya está registrado.';
    end if;
end;
//
delimiter ;
