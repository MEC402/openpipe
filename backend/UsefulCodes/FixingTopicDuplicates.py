

def fixingCultureDuplicates():
    from sqlalchemy import and_

    from openpipeAPI.ORM.ORM import ORM
    from openpipeAPI.ORM.TO import TO

    orm = ORM()
    tables = TO().getClasses()
    MetaTag = tables["metaTag"]
    res = orm.executeSelect(
        """SELECT value,topic_id FROM culture_tags""")
    ban=['North','probably','Western','Central','Northeastern','Northeast','Lower','Southern','possibly','Northern','South','Northwestern','Probably','Eastern','later','East','late','southern']
    m={}
    n=len(res['data'])
    for r in res['data']:
        v=r['value'][0]
        f=v.split(',')[0].split(' ')
        c=''
        if f[0] in ban:
            c=f[1]
        else:
            c=f[0]
        c=c.strip(";|)|(|?|/|:| |.")
        if c in m.keys():
            m[c].append(r["topic_id"][0])
        else:
            m[c]=[r["topic_id"][0]]
    print(n,len(m.keys()))
    ml=sorted(m.keys())

    for i in ml:
        print(i)
    print(m)
        # orm.session.query(MetaTag).filter(
        #     and_(MetaTag.metaDataId == r["metaDataId"][0], MetaTag.tagName == 'openpipe_canonical_biography')).update(
        #     {"value": r['value'][0]})

    # print(i,j,i+j)
    orm.commitClose()



fixingCultureDuplicates()