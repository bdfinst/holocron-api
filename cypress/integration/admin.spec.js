const setUp = (organizationName, valueStreamName) =>
  cy.apiCreateOrganization(organizationName).then(({ organization }) => {
    cy.apiCreateValueStream(valueStreamName, organization.id).then(
      ({ valuestream }) => {
        cy.wrap({
          organization,
          valuestream,
        })
      },
    )
  })

const tearDown = (team, organization, valueStream) => {
  const teamWasCreated = !!team
  const vsWasCreated = !!valueStream
  const orgWasCreated = !!organization
  if (teamWasCreated && vsWasCreated && orgWasCreated) {
    cy.apiDeleteTeam(team.id).then(() => {
      cy.apiDeleteValueStream(valueStream.id).then(() => {
        cy.apiDeleteOrganization(organization.id)
      })
    })
  } else if (!teamWasCreated && vsWasCreated && orgWasCreated) {
    cy.apiDeleteValueStream(valueStream.id).then(() => {
      cy.apiDeleteOrganization(organization.id)
    })
  } else if (!teamWasCreated && !vsWasCreated && orgWasCreated) {
    cy.apiDeleteOrganization(organization.id)
  }
}



describe('Test team CRUD', () => {
  const screenshotFolderName = 'test_team_crud'
  let dummyOrganization,
    dummyValueStream,
    teamName,
    orgName,
    vsName,
    dummyTeam,
    newTeamName,
    ticketBoardId

  beforeEach(cy.mockAuth)

  after(() => {
    tearDown(dummyTeam, dummyOrganization, dummyValueStream)
  })

  before(() => {
    teamName = cy.utils.randomName(8)
    orgName = cy.utils.randomName(8)
    vsName = cy.utils.randomName(8)

    setUp(orgName, vsName).then(({ organization, valuestream }) => {
      dummyOrganization = organization
      dummyValueStream = valuestream
    })
    cy.apiGetAvailableTicketBoard().then(({id})=>{
      ticketBoardId = id
    })

  })
  
  it('can create a team', () => {
    cy.apiCreateTeam(teamName,[ticketBoardId], 3, dummyValueStream.id).then(({team})=>{
        dummyTeam = team
    })
  })
  it('can update a team', ()=>{
    newTeamName = cy.utils.randomName(8)
    cy.apiUpdateTeam(newTeamName,[ticketBoardId], 3, dummyValueStream.id, dummyTeam.id)
  })
  it('can delete a team', ()=>{
    cy.apiDeleteTeam(dummyTeam.id)
  })
})
