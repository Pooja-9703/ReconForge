from dataclasses import dataclass, field
from reconforge.models.finding import Finding

@dataclass(slots=True)
class DNSResult:
    resolved_ip: str | None = None

    a_records: list[str] = field(default_factory=list)
    aaaa_records: list[str] = field(default_factory=list)

    mx_records: list[str] = field(default_factory=list)
    ns_records: list[str] = field(default_factory=list)

    txt_records: list[str] = field(default_factory=list)

    cname: str | None = None


@dataclass(slots=True)
class HTTPResult:
    status_code: int | None = None
    server: str | None = None
    content_type: str | None = None
    content_length: int | None = None
    redirect_url: str | None = None
    title: str | None = None
    response_time: float | None = None

    headers: dict[str, str] = field(default_factory=dict)

@dataclass(slots=True)
class TLSResult:
    subject: str | None = None
    issuer: str | None = None

    valid_from: str | None = None
    valid_until: str | None = None

    days_remaining: int | None = None

    sans: list[str] = field(default_factory=list)
    
    tls_version: str | None = None
    cipher: str | None = None

@dataclass(slots=True)
class PortInfo:
    port: int
    service: str
    banner: str | None = None


@dataclass(slots=True)
class PortScanResult:
    open_ports: list[PortInfo] = field(default_factory=list)


@dataclass(slots=True)
class WHOISResult:
    registrar: str | None = None
    creation_date: str | None = None
    expiration_date: str | None = None
    updated_date: str | None = None

    name_servers: list[str] = field(default_factory=list)

@dataclass(slots=True)
class TechnologyResult:
    technologies: list[str] = field(default_factory=list)

@dataclass(slots=True)
class ScanResults:
    dns: DNSResult = field(default_factory=DNSResult)
    http: HTTPResult = field(default_factory=HTTPResult)
    tls: TLSResult = field(default_factory=TLSResult)
    ports: PortScanResult = field(default_factory=PortScanResult)
    whois: WHOISResult = field(default_factory=WHOISResult)
    technology: TechnologyResult = field(default_factory=TechnologyResult)

    findings: list[Finding] = field(default_factory=list)