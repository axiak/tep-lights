
cdef extern from "sexp.h":
    ctypedef enum elt_t:
        SEXP_VALUE
        SEXP_LIST

    ctypedef enum parsermode_t:
        PARSER_NORMAL
        PARSER_INLINE_BINARY
        PARSER_EVENTS_ONLY

    ctypedef enum atom_t:
        SEXP_BASIC
        SEXP_SQUOTE
        SEXP_DQUOTE
        SEXP_BINARY

    ctypedef struct sexp_t:
        atom_t aty
        char * bindata
        size_t binlength
        sexp_t* list
        sexp_t* next
        elt_t ty
        char * val
        size_t val_allocated
        size_t val_used

    ctypedef struct stack_lvl_t:
        stack_lvl_t * above
        stack_lvl_t * below
        void * data

    ctypedef struct faststack_t:
        stack_lvl_t *top
        stack_lvl_t *bottom
        int height

    cdef enum sexp_errcode_t:
        SEXP_ERR_OK = 0
        SEXP_ERR_MEMORY
        SEXP_ERR_BADFORM
        SEXP_ERR_BADCONTENT
        SEXP_ERR_NULLSTRING
        SEXP_ERR_IO
        SEXP_ERR_IO_EMPTY
        SEXP_ERR_MEM_LIMIT
        SEXP_ERR_BUFFER_FULL
        SEXP_ERR_BAD_PARAM
        SEXP_ERR_BAD_STACK
        SEXP_ERR_UNKNOWN_STATE

    ctypedef struct parser_event_handlers_t:
        pass

    ctypedef struct pcont_t:
        faststack_t* stack
        sexp_t* last_sexp
        char * val
        size_t val_allocated
        size_t val_used
        char * vcur
        char * lastPos
        char * sbuffer
        unsigned int depth
        unsigned int qdepth
        unsigned int state
        unsigned int esc
        unsigned int squoted
        sexp_errcode_t error
        parsermode_t mode
        size_t binexpected
        size_t binread
        char * bindata
        parser_event_handlers_t * event_handlers

    sexp_t * iparse_sexp(char * s, size_t len, pcont_t* cc)
    sexp_t * copy_sexp(sexp_t * s)
    faststack_t * make_stack()
    stack_lvl_t* pop(faststack_t * s)
    faststack_t* push(faststack_t * cur_stack,
                      void * data)
    pcont_t * cparse_sexp(char * s, size_t len, pcont_t* cc)
    pcont_t * init_continuation(char * buf)

    void destroy_continuation(pcont_t * cc)
    void destroy_sexp(sexp_t * sx)
    void destroy_stack(faststack_t * s)

SEXP_ERROR_DICT = {
    0: 'SEXP_ERR_OK',
    1: 'SEXP_ERR_MEMORY',
    2: 'SEXP_ERR_BADFORM',
    3: 'SEXP_ERR_BADCONTENT',
    4: 'SEXP_ERR_NULLSTRING',
    5: 'SEXP_ERR_IO',
    6: 'SEXP_ERR_IO_EMPTY',
    7: 'SEXP_ERR_MEM_LIMIT',
    8: 'SEXP_ERR_BUFFER_FULL',
    9: 'SEXP_ERR_BAD_PARAM',
    10: 'SEXP_ERR_BAD_STACK',
    11: 'SEXP_ERR_UNKNOWN_STATE'
    }

#cdef int SEXP_VALUE = 0
#cdef int SEXP_LIST = 1

#cdef int SEXP_BASIC = 0
#cdef int SEXP_SQUOTE = 1
#cdef int SEXP_DQUOTE = 2
#cdef int SEXP_BINARY = 3

