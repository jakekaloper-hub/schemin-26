export const CHRONICLE_SPREAD_PIPELINE={
  id:"chronicle-spread-v1",
  stages:[
    {id:"source_packet",worker:"librarian",gate:"sourceGate"},
    {id:"manuscript_slice",worker:"beatWriter",gate:"canonGate"},
    {id:"spread_spec",worker:"architect",gate:"preflightGate"},
    {id:"art_job",worker:"visualDevelopment",gate:"characterVisionGate"},
    {id:"composition",worker:"compositor",gate:"renderGate"},
    {id:"final_qa",worker:"umpire",gate:"closerGate"}
  ]
};
