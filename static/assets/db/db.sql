drop database if exists yadmandul_store;
create database yadmandul_store;
use yadmandul_store;

create table administradores(
	id_admin int primary key auto_increment,
    nom_admin varchar(30) not null,
    ap_pat_admin varchar(30) not null,
    ap_mat_admin varchar(30) not null,
    fec_nac_admin date not null,
    correo_admin varchar(255) not null,
    password_admin varchar(255) not null,
    foto_admin varchar(255) not null
) engine = InnoDB;

create table clientes(
	id_cli int primary key auto_increment,
    nom_cli varchar(30) not null,
    ap_pat_cli varchar(30) not null,
    ap_mat_cli varchar(30) not null,
    fecha_nac_cli date not null,
    correo_cli varchar(255) not null,
    password_cli varchar(255) not null,
    estado_cli boolean not null,
    foto_cli varchar(255) not null
) engine = InnoDB;

create table empleados(
	id_emp int primary key auto_increment,
    nom_emp varchar(30) not null,
    ap_pat_emp varchar(30) not null,
    ap_mat_emp varchar(30) not null,
    fec_nac_emp date not null,
    correo_emp varchar(255),
    password_emp varchar(255) not null,
    estado_emp boolean not null,
    foto_emp varchar(255) not null
) engine = InnoDB;

create table proveedores(
	id_prov int primary key auto_increment,
    nom_prov varchar(30) not null,
    ap_pat_prov varchar(30) not null,
    ap_mat_prov varchar(30) not null,
    correo_prov varchar(255) not null,
    tel_prov varchar(10) not null
) engine = InnoDB;

create table productos(
	id_prod int primary key auto_increment,
    nom_prod varchar(30) not null,
    tipo_prod varchar(30) not null,
    precio_prod double not null,
    cantidad_prod int not null,
    estado_prod boolean not null,
    foto_prod varchar(255) not null, -- Quitar para la presentacion
    id_prov int not null,
    foreign key (id_prov) references proveedores(id_prov)
) engine = InnoDB;

create table ventas(
	id_venta int primary key auto_increment,
    id_emp int not null,
    id_cli int not null,
    fec_venta date not null,
    hor_venta time not null,
    total_venta double not null,
    foreign key (id_emp) references empleados(id_emp),
    foreign key (id_cli) references clientes(id_cli)
) engine = InnoDB;

create table detalle_venta(
	id_venta int not null,
    id_prod int not null,
    cantidad int not null,
    importe double not null,
    foreign key (id_venta) references ventas(id_venta),
    foreign key (id_prod) references productos(id_prod)
) engine = InnoDB;

create table carrito(
	id_cli int not null,
    id_prod int not null,
    cantidad int not null,
    total double not null,
    foreign key (id_cli) references clientes(id_cli),
    foreign key (id_prod) references productos(id_prod)
) engine = InnoDB;

create table pedidos(
	id_pedido int primary key auto_increment,
    id_cli int not null,
    fec_pedido date not null,
    hor_pedido time not null,
    total double not null,
    pendiente boolean not null,
    cancelado boolean not null
) engine = InnoDB;

create table detalle_pedidos(
	id_pedido int not null,
    id_prod int not null,
    cantidad int not null,
    importe double not null,
    detalles varchar(50) not null,
    foreign key (id_pedido) references pedidos(id_pedido),
    foreign key (id_prod) references productos(id_prod)
) engine = InnoDB;

create table estado_pedidos(
	id_pedido int not null,
    id_emp int not null,
    estado varchar(30) not null,
    foreign key (id_pedido) references pedidos(id_pedido),
    foreign key (id_emp) references empleados(id_emp)
) engine = InnoDB;
