describe('Test team CRUD', () => {
  let organization, valueStream, team, mockUser

  after(() => {
    if (!!team && !!valueStream && !!organization) {
      cy.apiDeleteTeam(team.id).then(() => {
        return cy.apiDeleteValueStream(valueStream.id)
      }).then(() => {
        return cy.apiDeleteOrganization(organization.id)
      })
    } else if (!team && !!valueStream && !!organization) {
      cy.apiDeleteValueStream(valueStream.id).then(() => {
        return cy.apiDeleteOrganization(organization.id)
      })
    } else if (!team && !valueStream && !!organization) {
      cy.apiDeleteOrganization(organization.id)
    }
  })

  before(() => {
    cy.apiCreateMockUser().then(response => {
      mockUser = JSON.parse(response.headers['x-user'])
      return cy.apiCreateOrganization({
        name: cy.utils.randomName(8),
        userIds: [mockUser.id],
      })
    }).then(response => {
      organization = response.body
      return cy.apiCreateValueStream({
        name: cy.utils.randomName(8),
        userIds: [mockUser.id],
        organizationId: organization.id
      })
    }).then(response => {
      valueStream = response.body
    })
  })
  
  it('can create a team', () => {
    cy.apiCreateTeam({
      name: cy.utils.randomName(8),
      teamSize: 5,
      userIds: [mockUser.id],
      valuestreamId: valueStream.id,
      collectorTargetIds: [],
    }).then(response => {
      team = response.body
    })
  })

  it('can update a team', ()=>{
    cy.apiUpdateTeam(team.id, {
      name: team.name,
      teamSize: 3,
      userIds: [mockUser.id],
      valuestreamId: valueStream.id,
      collectorTargetIds: [],
    })
  })

  it('can delete a team', ()=>{
    cy.apiDeleteTeam(team.id)
  })
})
